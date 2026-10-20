import { expect, test } from "vitest";

import { makeTimetable } from "#test/fixtures.ts";

import type { LocationId } from "./data/locations.ts";
import type { Itinerary, Selection } from "./itinerary.ts";
import { makeItineraries, type PlanOptions } from "./route.ts";
import { type SelectOptions, selectItineraries } from "./search.ts";

const timetable = makeTimetable();
const DATE = Date.UTC(2026, 9, 8);
const OPTIONS: PlanOptions = { date: DATE, checkin: "reservation", early: 15, long: false };
// The evening before, when no itinerary has departed.
const BEFORE = "2026-10-07T20:00:00";

const plansFor = (origin: LocationId, destination: LocationId): Itinerary[] => {
    return makeItineraries(origin, destination, OPTIONS, timetable, DATE);
};

/** Select itineraries with the default options, unless overridden. */
const pick = (itineraries: Itinerary[], now: string, options: Partial<SelectOptions> = {}): Selection => {
    return selectItineraries(itineraries, now, { all: false, sort: "duration", underway: false, ...options });
};

/** Summarize itineraries as their route and times. */
const summarize = (itineraries: Itinerary[]): string[] => {
    return itineraries.map(
        (itinerary) => `${itinerary.route} ${itinerary.depart.slice(11, 16)}>${itinerary.arrive.slice(11, 16)}`,
    );
};

const SUNSHINE_COAST = "vancouver-HSB-LNG-ERL-SLT-PWR-TEX-van_anda";

// The expected results below are planner output for the feed in `test/fixtures`, reviewed by hand.

test("selectItineraries returns the ten fastest itineraries across routes", () => {
    const found = pick(plansFor("vancouver", "van_anda"), BEFORE);

    expect(summarize(found.itineraries)).toEqual([
        `${SUNSHINE_COAST} 15:35>22:39`,
        `${SUNSHINE_COAST} 06:20>13:34`,
        `${SUNSHINE_COAST} 11:00>18:44`,
        `${SUNSHINE_COAST} 08:40>16:49`,
        "vancouver-HSB-NAN-CMX-PWR-TEX-van_anda 09:55>18:44",
        "vancouver-TSA-DUK-CMX-PWR-TEX-van_anda 03:59>13:34",
        "vancouver-TSA-DUK-CMX-PWR-TEX-van_anda 08:59>18:44",
        "vancouver-HSB-NAN-CMX-PWR-TEX-van_anda 12:15>22:39",
        "vancouver-TSA-SWB-CMX-PWR-TEX-van_anda 11:44>22:39",
        "vancouver-TSA-SWB-CMX-PWR-TEX-van_anda 07:44>18:44",
    ]);
    expect(found.more).toBe(1);
    expect(found.departed).toBe(0);
});

test("selectItineraries returns the ten earliest departures if sorted by departure", () => {
    const found = pick(plansFor("vancouver", "van_anda"), BEFORE, { sort: "departure" });

    expect(summarize(found.itineraries).slice(0, 4)).toEqual([
        "vancouver-TSA-DUK-CMX-PWR-TEX-van_anda 03:59>13:34",
        `${SUNSHINE_COAST} 06:20>13:34`,
        "vancouver-TSA-SWB-CMX-PWR-TEX-van_anda 07:44>18:44",
        `${SUNSHINE_COAST} 08:40>16:49`,
    ]);
    expect(found.itineraries).toHaveLength(10);
    expect(found.more).toBe(1);
});

test("journey that changes vessels at a terminal has one sailing to it and one from it", () => {
    // No vessel sails from Little River to Blubber Bay: one goes to Westview, and another from there.
    const found = pick(plansFor("victoria", "van_anda"), BEFORE);

    expect(summarize(found.itineraries).slice(0, 4)).toEqual(
        ["02:32>09:29", "11:47>18:44", "15:42>22:39", "06:27>13:34"].map(
            (times) => `victoria-CMX-PWR-TEX-van_anda ${times}`,
        ),
    );
    expect(found.itineraries[0]?.steps.filter((step) => step.kind === "FERRY")).toMatchObject([
        { description: "Ferry sailing from Little River Terminal to Westview Terminal", from: "CMX", to: "PWR" },
        { description: "Ferry sailing from Westview Terminal to Blubber Bay Terminal", from: "PWR", to: "TEX" },
    ]);
});

test("departed itineraries are excluded and counted", () => {
    const found = pick(plansFor("vancouver", "van_anda"), "2026-10-08T09:00:00", { sort: "departure" });

    expect(found.itineraries[0]?.depart).toBe("2026-10-08T09:55:50");
    expect(found.itineraries).toHaveLength(6);
    expect(found.departed).toBe(12);
    expect(found.more).toBe(0);
});

test("no itineraries are returned after all have departed", () => {
    const found = pick(plansFor("vancouver", "van_anda"), "2026-10-08T16:00:00");

    expect(found).toMatchObject({ itineraries: [], more: 0, departed: 22 });
});

test("all returns every itinerary, starting with the default selection", () => {
    const plans = plansFor("vancouver", "van_anda");
    const first = pick(plans, BEFORE);

    const found = pick(plans, BEFORE, { all: true });

    expect(found.itineraries).toHaveLength(11);
    expect(found.more).toBe(0);
    expect(found.itineraries.slice(0, 10)).toEqual(first.itineraries);
});

test("drive with no ferry is an itinerary", () => {
    const found = pick(plansFor("hope", "TSA"), BEFORE);

    expect(found.itineraries).toEqual([expect.objectContaining({ duration: 6598, drivingDistance: 163.7894 })]);
    expect(found.itineraries[0]?.steps.map((step) => step.kind)).toEqual(["MARK", "DRIVE", "MARK"]);
});

test("itinerary lists its steps with their kinds, and the terminals and schedule URLs of its sailings", () => {
    const found = pick(plansFor("vancouver", "van_anda"), BEFORE);
    const itinerary = found.itineraries.find((itinerary) => itinerary.depart === "2026-10-08T06:20:50");

    expect(itinerary).toMatchObject({
        id: expect.stringMatching(/^[0-9a-z]{11}$/),
        depart: "2026-10-08T06:20:50",
        arrive: "2026-10-08T13:34:24",
        duration: 26014,
        drivingDistance: 144.42090000000002,
        mapUrl: expect.stringContaining("https://www.google.com/maps/dir/"),
    });
    expect(itinerary?.steps.map((step) => step.kind)).toEqual([
        "MARK",
        "DRIVE",
        "WAIT",
        "FERRY",
        "DRIVE",
        "FREE",
        "WAIT",
        "FERRY",
        "DRIVE",
        "FREE",
        "WAIT",
        "FERRY",
        "DRIVE",
        "MARK",
    ]);
    expect(itinerary?.steps[0]).toEqual({
        kind: "MARK",
        start: "2026-10-08T06:20:50",
        end: "2026-10-08T06:20:50",
        description: "Depart from Vancouver",
    });
    expect(itinerary?.steps[3]).toEqual({
        kind: "FERRY",
        start: "2026-10-08T07:30:00",
        end: "2026-10-08T08:10:00",
        description: "Ferry sailing from Horseshoe Bay Terminal to Langdale Terminal",
        scheduleUrl: "https://www.bcferries.com/routes-fares/schedules/daily/HSB-LNG?&scheduleDate=10/08/2026",
        from: "HSB",
        to: "LNG",
    });
});

// Each rule separately, with made-up itineraries.

interface MadeUpPlan {
    /** Location IDs separated by spaces, with `~` before those reached by ferry. */
    route: string;
    depart: string;
    arrive: string;
}

const makePlan = ({ route, depart, arrive }: MadeUpPlan, index: number): Itinerary => {
    const stops = route.split(" ");
    const start = `2026-10-08T${depart}:00`;
    const end = `2026-10-08T${arrive}:00`;
    return {
        id: String(index).padStart(11, "0"),
        route: stops.map((stop) => stop.replace("~", "")).join("-"),
        depart: start,
        arrive: end,
        duration: (Date.parse(`${end}Z`) - Date.parse(`${start}Z`)) / 1000,
        drivingDistance: 0,
        mapUrl: "",
        steps: stops.filter((stop) => stop.startsWith("~")).map(() => ({ kind: "FERRY", start, end, description: "" })),
    };
};

const select = (madeUp: MadeUpPlan[], all = false) => {
    const plans = madeUp.map(makePlan);
    return summarize(pick(plans, BEFORE, { all }).itineraries);
};

test("itinerary is excluded if another on its route departs no earlier and arrives no later", () => {
    expect(
        select([
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~B", depart: "07:00", arrive: "10:00" },
            { route: "A ~B", depart: "08:00", arrive: "11:00" },
        ]),
    ).toEqual(["A-B 08:00>10:00"]);
});

test("itinerary is kept if it departs later or arrives earlier than every other on its route", () => {
    expect(
        select([
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~B", depart: "09:00", arrive: "12:00" },
            { route: "A ~B", depart: "06:00", arrive: "09:00" },
        ]),
    ).toEqual(["A-B 08:00>10:00", "A-B 06:00>09:00", "A-B 09:00>12:00"]);
});

test("itinerary is kept if only itineraries on other routes are better", () => {
    expect(
        select([
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~C ~B", depart: "07:00", arrive: "10:00" },
            { route: "A ~D ~B", depart: "08:00", arrive: "11:00" },
        ]),
    ).toEqual(["A-B 08:00>10:00", "A-C-B 07:00>10:00", "A-D-B 08:00>11:00"]);
});

test("one of two itineraries on a route with the same times is kept", () => {
    expect(
        select([
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
        ]),
    ).toEqual(["A-B 08:00>10:00"]);
});

const FOUR: MadeUpPlan[] = [
    { route: "A ~C ~B", depart: "12:00", arrive: "15:00" },
    { route: "A ~B", depart: "13:00", arrive: "17:00" },
    { route: "A ~B", depart: "07:00", arrive: "09:00" },
    { route: "A ~C ~B", depart: "08:00", arrive: "11:30" },
];

test.each([
    ["duration", ["A-B 07:00>09:00", "A-C-B 12:00>15:00", "A-C-B 08:00>11:30", "A-B 13:00>17:00"]],
    ["departure", ["A-B 07:00>09:00", "A-C-B 08:00>11:30", "A-C-B 12:00>15:00", "A-B 13:00>17:00"]],
    ["arrival", ["A-B 07:00>09:00", "A-C-B 08:00>11:30", "A-C-B 12:00>15:00", "A-B 13:00>17:00"]],
] as const)("itineraries are sorted by %s across routes", (sort, expected) => {
    expect(summarize(pick(FOUR.map(makePlan), BEFORE, { sort }).itineraries)).toEqual(expected);
});

/** Twelve 30-minute itineraries that depart an hour apart from 06:00, each on its own route. */
const TWELVE: MadeUpPlan[] = Array.from({ length: 12 }, (_, index) => {
    const hour = String(6 + index).padStart(2, "0");
    return { route: `A ~${index} ~B`, depart: `${hour}:00`, arrive: `${hour}:30` };
});

test("only the first ten itineraries are returned unless all is set, and the rest are counted", () => {
    const found = pick(TWELVE.map(makePlan).toReversed(), BEFORE, { sort: "departure" });

    expect(found.itineraries.map((itinerary) => itinerary.depart.slice(11, 16))).toEqual(
        ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15"].map((hour) => `${hour}:00`),
    );
    expect(found.more).toBe(2);
    expect(pick(TWELVE.map(makePlan), BEFORE, { all: true })).toMatchObject({
        itineraries: { length: 12 },
        more: 0,
    });
});

const THROUGH_THE_DAY: MadeUpPlan[] = [
    { route: "A ~B", depart: "06:00", arrive: "08:00" },
    { route: "A ~B", depart: "09:00", arrive: "11:00" },
    { route: "A ~B", depart: "12:00", arrive: "14:00" },
];

test("departed count includes itineraries that are under way", () => {
    const found = pick(THROUGH_THE_DAY.map(makePlan), "2026-10-08T10:00:00");

    expect(summarize(found.itineraries)).toEqual(["A-B 12:00>14:00"]);
    expect(found).toMatchObject({ departed: 2, underway: 1 });
});

test("underway includes itineraries that are under way and excludes those that have arrived", () => {
    const found = pick(THROUGH_THE_DAY.map(makePlan), "2026-10-08T10:00:00", { underway: true });

    expect(summarize(found.itineraries)).toEqual(["A-B 09:00>11:00", "A-B 12:00>14:00"]);
    expect(found).toMatchObject({ departed: 1, underway: 0 });
});
