import { expect, test } from "vitest";
import { makeTimetable } from "#test/fixtures.ts";
import type { Itinerary } from "./api";
import type { LocationId } from "./data/locations";
import { type PlanOptions, type RoutePlan, routePlans } from "./route";
import { findItinerary, selectItineraries } from "./search";

const timetable = makeTimetable();
const DATE = Date.UTC(2026, 9, 8);
const OPTIONS: PlanOptions = { date: DATE, showAll: false, assured: false, hostled: false, buffer: 15 };
// The evening before, when nothing has left yet.
const BEFORE = "2026-10-07T20:00:00";

const plansFor = (origin: LocationId, destination: LocationId): RoutePlan[] => {
    return routePlans(origin, destination, OPTIONS, timetable, DATE);
};

/** Lay itineraries out as the locations of their route and their times, to compare them at a glance. */
const summarize = (itineraries: Itinerary[]): string[] => {
    return itineraries.map(
        (itinerary) => `${itinerary.route} ${itinerary.depart.slice(11, 16)}>${itinerary.arrive.slice(11, 16)}`,
    );
};

const SUNSHINE_COAST = "vancouver-HSB-LNG-ERL-SLT-PWR-TEX-van_anda";

// The expected results below were worked out apart from this code, from the route plans of the deployed API.

test("journey over several ferries shows the one route worth taking", () => {
    const plans = plansFor("vancouver", "van_anda");

    const found = selectItineraries(plans, BEFORE);

    expect(summarize(found.itineraries)).toEqual([
        `${SUNSHINE_COAST} 06:20>13:34`,
        `${SUNSHINE_COAST} 08:40>16:49`,
        `${SUNSHINE_COAST} 11:00>18:44`,
        `${SUNSHINE_COAST} 15:35>22:39`,
    ]);
    expect(found.moreRoutes).toBe(8);
    expect(found.departed).toBe(0);
});

test("journey over several ferries back shows the same route", () => {
    const plans = plansFor("van_anda", "vancouver");

    const found = selectItineraries(plans, BEFORE);

    expect(summarize(found.itineraries)).toEqual(
        ["07:10>14:19", "08:50>16:39", "11:15>18:59", "14:25>21:19", "16:20>23:34"].map(
            (times) => `van_anda-TEX-PWR-SLT-ERL-LNG-HSB-vancouver ${times}`,
        ),
    );
});

test("journey by way of a terminal where the vessel is changed has a sailing to it and another from it", () => {
    // No vessel sails from Little River to Blubber Bay: one goes to Westview, and another from there.
    const plans = plansFor("victoria", "van_anda");

    const found = selectItineraries(plans, BEFORE);

    expect(summarize(found.itineraries)).toEqual(
        ["02:32>09:29", "06:27>13:34", "11:47>18:44", "15:42>22:39"].map(
            (times) => `victoria-CMX-PWR-TEX-van_anda ${times}`,
        ),
    );
    expect(found.itineraries[0]?.steps.filter((step) => step.kind === "FERRY")).toMatchObject([
        { description: "Ferry sailing from Little River Terminal to Westview Terminal", from: "CMX", to: "PWR" },
        { description: "Ferry sailing from Westview Terminal to Blubber Bay Terminal", from: "PWR", to: "TEX" },
    ]);
});

test("journey over one ferry shows the route that is fastest through the day and the one that runs latest", () => {
    const plans = plansFor("vancouver", "victoria");

    const found = selectItineraries(plans, BEFORE);

    expect(summarize(found.itineraries)).toEqual([
        ...[
            ...["04:44>08:02", "05:44>09:02", "06:44>10:02", "07:44>11:02", "08:44>12:02", "09:44>13:02"],
            ...["10:44>14:02", "11:44>15:02", "12:44>16:02", "13:44>17:02", "14:44>18:02", "15:44>19:02"],
            ...["17:44>21:02", "18:44>22:02", "19:44>23:02"],
        ].map((times) => `vancouver-TSA-SWB-victoria ${times}`),
        "vancouver-HSB-NAN-victoria 21:30>01:50",
    ]);
    expect(found.moreRoutes).toBe(20);
});

test("journey between terminals shows the sailing that calls on the way and the faster ones over two sailings", () => {
    const plans = plansFor("TSA", "PST");

    const found = selectItineraries(plans, BEFORE);

    expect(summarize(found.itineraries)).toEqual([
        "TSA-SWB-PST 06:15>10:20",
        "TSA-SWB-PST 12:15>16:25",
        "TSA-PST 18:45>21:57",
    ]);
});

test("itineraries that have already left are left out and counted", () => {
    const plans = plansFor("vancouver", "van_anda");

    const found = selectItineraries(plans, "2026-10-08T09:00:00");

    expect(summarize(found.itineraries)).toEqual([`${SUNSHINE_COAST} 11:00>18:44`, `${SUNSHINE_COAST} 15:35>22:39`]);
    expect(found.departed).toBe(17);
    expect(found.moreRoutes).toBe(8);
});

test("no itineraries are left once every one has left", () => {
    const found = selectItineraries(plansFor("vancouver", "van_anda"), "2026-10-08T16:00:00");

    expect(found).toMatchObject({ itineraries: [], moreRoutes: 0, departed: 34 });
});

test("all routes are shown when asked for, each with its own best itineraries", () => {
    const plans = plansFor("vancouver", "van_anda");
    const best = selectItineraries(plans, BEFORE);

    const found = selectItineraries(plans, BEFORE, { all: true });

    expect(new Set(found.itineraries.map((itinerary) => itinerary.route)).size).toBe(9);
    expect(found.moreRoutes).toBe(0);
    expect(found.itineraries).toEqual(expect.arrayContaining(best.itineraries));
    const departures = found.itineraries.map((itinerary) => itinerary.depart);
    expect(departures).toEqual(departures.toSorted());
});

test("drive without a sailing is an itinerary", () => {
    const found = selectItineraries(plansFor("hope", "TSA"), BEFORE);

    expect(found.itineraries).toEqual([expect.objectContaining({ duration: 6598, drivingDistance: 163.7894 })]);
    expect(found.itineraries[0]?.steps.map((step) => step.kind)).toEqual(["MARK", "DRIVE", "MARK"]);
});

test("itinerary lists its steps with their kinds, and the terminals and schedules of its sailings", () => {
    const found = selectItineraries(plansFor("vancouver", "van_anda"), BEFORE);
    const [itinerary] = found.itineraries;

    expect(itinerary).toMatchObject({
        id: "ce6c2a2222aa",
        depart: "2026-10-08T06:20:50",
        arrive: "2026-10-08T13:34:24",
        duration: 26014,
        drivingDistance: 144.42090000000002,
        mapUrl: expect.stringContaining("https://www.google.com/maps/dir/"),
    });
    expect(itinerary?.steps.map((step) => step.kind)).toEqual([
        ...["MARK", "DRIVE", "WAIT", "FERRY", "DRIVE", "FREE", "WAIT", "FERRY"],
        ...["DRIVE", "FREE", "WAIT", "FERRY", "DRIVE", "MARK"],
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

test("itinerary is found by its ID among all there are, shown or not", () => {
    const plans = plansFor("vancouver", "van_anda");
    const shown = selectItineraries(plans, BEFORE).itineraries;
    const hidden = selectItineraries(plans, BEFORE, { all: true }).itineraries.find(
        (itinerary) => itinerary.route !== SUNSHINE_COAST,
    );

    expect(findItinerary(plans, "ce6c2a2222aa")).toEqual(shown[0]);
    expect(findItinerary(plans, hidden?.id ?? "")).toEqual(hidden);
});

test("no itinerary is found by an ID that none has", () => {
    const plans = plansFor("vancouver", "van_anda");

    expect(findItinerary(plans, "000000000000")).toBeUndefined();
    expect(findItinerary(plans, "")).toBeUndefined();
    // Only a whole ID finds an itinerary.
    expect(findItinerary(plans, "ce6c2a")).toBeUndefined();
});

// The rules one at a time, with route plans made up for them.

interface MadeUpPlan {
    /** Locations gone through, with a `~` before those reached by ferry. */
    route: string;
    depart: string;
    arrive: string;
    driving?: number;
}

const makePlan = ({ route, depart, arrive, driving = 0 }: MadeUpPlan, index: number): RoutePlan => {
    const stops = route.split(" ");
    const start = `2026-10-08T${depart}:00`;
    const end = `2026-10-08T${arrive}:00`;
    return {
        hash: String(index).padStart(12, "0"),
        depart_time: start,
        arrive_time: end,
        duration: (Date.parse(`${end}Z`) - Date.parse(`${start}Z`)) / 1000,
        driving_duration: 0,
        driving_distance: driving,
        map_url: "",
        segments: stops.slice(1).map((stop, index) => ({
            connection: {
                id: "",
                origin: { id: stops[index]?.replace("~", "") },
                destination: { id: stop.replace("~", "") },
                duration: 0,
                distance: 0,
                fuel: 0,
                type: stop.startsWith("~") ? "FERRY" : "CAR",
            },
            times: [],
        })),
    } as unknown as RoutePlan;
};

const select = (madeUp: MadeUpPlan[], all = false) => {
    const plans = madeUp.map(makePlan);
    return summarize(selectItineraries(plans, BEFORE, { all }).itineraries);
};

test("itinerary is left out when another leaves no earlier and arrives no later", () => {
    expect(
        select([
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~C ~B", depart: "07:00", arrive: "10:00" },
            { route: "A ~D ~B", depart: "08:00", arrive: "11:00" },
        ]),
    ).toEqual(["A-B 08:00>10:00"]);
});

test("itinerary is kept when it leaves later or arrives earlier than every other", () => {
    expect(
        select([
            { route: "A ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~C ~B", depart: "09:00", arrive: "12:00" },
            { route: "A ~D ~B", depart: "06:00", arrive: "09:00" },
        ]),
    ).toEqual(["A-D-B 06:00>09:00", "A-B 08:00>10:00", "A-C-B 09:00>12:00"]);
});

test("itinerary is kept when the only ones better in time use more ferries", () => {
    expect(
        select([
            { route: "A ~C ~B", depart: "08:00", arrive: "10:00" },
            { route: "A ~B", depart: "07:00", arrive: "11:00" },
        ]),
    ).toEqual(["A-B 07:00>11:00", "A-C-B 08:00>10:00"]);
});

test("of itineraries with the same times and ferries, the one with the least driving is kept", () => {
    expect(
        select([
            { route: "A C ~B", depart: "08:00", arrive: "10:00", driving: 50 },
            { route: "A D ~B", depart: "08:00", arrive: "10:00", driving: 20 },
            { route: "A E ~B", depart: "08:00", arrive: "10:00", driving: 30 },
        ]),
    ).toEqual(["A-D-B 08:00>10:00"]);
});

test("itineraries are in order of departure, whatever their route", () => {
    expect(
        select([
            { route: "A ~C ~B", depart: "12:00", arrive: "15:00" },
            { route: "A ~B", depart: "13:00", arrive: "17:00" },
            { route: "A ~B", depart: "07:00", arrive: "09:00" },
            { route: "A ~C ~B", depart: "08:00", arrive: "11:30" },
        ]),
    ).toEqual(["A-B 07:00>09:00", "A-C-B 08:00>11:30", "A-C-B 12:00>15:00", "A-B 13:00>17:00"]);
});

const FOUR_ROUTES: MadeUpPlan[] = [
    { route: "A ~B", depart: "06:00", arrive: "07:00" },
    { route: "A ~C ~B", depart: "07:00", arrive: "09:00" },
    { route: "A ~D ~B", depart: "08:00", arrive: "11:00" },
    { route: "A ~E ~B", depart: "09:00", arrive: "13:00" },
    // Never worth taking, as the first route leaves at the same time and arrives earlier.
    { route: "A ~F ~B", depart: "06:00", arrive: "12:00" },
    { route: "A ~F ~B", depart: "05:00", arrive: "12:00" },
];

test("only the three routes with the fastest itineraries are shown unless all are asked for", () => {
    const plans = FOUR_ROUTES.map(makePlan);

    const found = selectItineraries(plans, BEFORE);

    expect(summarize(found.itineraries)).toEqual(["A-B 06:00>07:00", "A-C-B 07:00>09:00", "A-D-B 08:00>11:00"]);
    expect(found.moreRoutes).toBe(2);
});

test("route that is never worth taking shows its own best itineraries when all are asked for", () => {
    expect(select(FOUR_ROUTES, true)).toEqual([
        "A-B 06:00>07:00",
        "A-F-B 06:00>12:00",
        "A-C-B 07:00>09:00",
        "A-D-B 08:00>11:00",
        "A-E-B 09:00>13:00",
    ]);
});

// All worth taking, as each leaves later and arrives later than the one before, but for the last, which is fastest.
const FOUR_TIMES: MadeUpPlan[] = [
    { route: "A ~C ~B", depart: "06:00", arrive: "09:00" },
    { route: "A ~D ~B", depart: "07:00", arrive: "10:30" },
    { route: "A ~E ~B", depart: "08:00", arrive: "12:30" },
    { route: "A ~F ~B", depart: "12:00", arrive: "13:00" },
];

test.each([
    ["duration", ["A-C-B", "A-D-B", "A-F-B"]],
    ["departure", ["A-C-B", "A-D-B", "A-E-B"]],
    ["arrival", ["A-C-B", "A-D-B", "A-E-B"]],
] as const)("routes shown are the three best by %s when that is what they are wanted in order of", (sort, routes) => {
    const found = selectItineraries(FOUR_TIMES.map(makePlan), BEFORE, { sort });

    expect(found.itineraries.map((itinerary) => itinerary.route)).toEqual(routes);
    expect(found.moreRoutes).toBe(1);
});

const THROUGH_THE_DAY: MadeUpPlan[] = [
    { route: "A ~B", depart: "06:00", arrive: "08:00" },
    { route: "A ~B", depart: "09:00", arrive: "11:00" },
    { route: "A ~B", depart: "12:00", arrive: "14:00" },
];

test("itineraries that have left count those still under way", () => {
    const found = selectItineraries(THROUGH_THE_DAY.map(makePlan), "2026-10-08T10:00:00");

    expect(summarize(found.itineraries)).toEqual(["A-B 12:00>14:00"]);
    expect(found).toMatchObject({ departed: 2, underway: 1 });
});

test("itineraries still under way are shown when asked for, and those that have arrived are not", () => {
    const found = selectItineraries(THROUGH_THE_DAY.map(makePlan), "2026-10-08T10:00:00", { underway: true });

    expect(summarize(found.itineraries)).toEqual(["A-B 09:00>11:00", "A-B 12:00>14:00"]);
    expect(found).toMatchObject({ departed: 1, underway: 0 });
});
