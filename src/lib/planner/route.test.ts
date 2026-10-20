import { expect, test } from "vitest";

import { POPULAR_ROUTES } from "#lib/popular.ts";
import { makeTimetable } from "#test/fixtures.ts";
import plans from "#test/fixtures/plans.json";
import routes from "#test/fixtures/routes.json";
import { summarize } from "#test/summary.ts";

import type { LocationId } from "./data/locations.ts";
import { findRoutes, makeItineraries, type PlanOptions } from "./route.ts";
import { parseLocal } from "./time.ts";

const timetable = makeTimetable();
const DATE = Date.UTC(2026, 9, 8);
const NOW = Date.UTC(2026, 9, 8, 13, 45, 10);
const OPTIONS: PlanOptions = { date: DATE, checkin: "reservation", early: 15, long: false };

test.each(Object.entries(routes))("findRoutes returns the expected routes for %s", (id, expected) => {
    const [origin, destination] = id.split("-") as [LocationId, LocationId];

    const found = findRoutes(origin, destination).map((route) => route.join("-"));

    expect(found).toHaveLength(expected.count);
    if ("listed" in expected) {
        expect(found).toEqual(expected.listed);
    }
});

test.each(plans)("makeItineraries returns the expected itineraries for $request", (expected) => {
    const { origin, destination, date, ...options } = expected.request as Partial<PlanOptions> & {
        origin: LocationId;
        destination: LocationId;
        date: string;
    };

    const found = makeItineraries(
        origin,
        destination,
        { ...OPTIONS, ...options, date: parseLocal(date) ?? Number.NaN },
        timetable,
        NOW,
    );

    expect(found).toHaveLength(expected.count);
    if ("listed" in expected) {
        expect(found.map(summarize)).toEqual(expected.listed);
    }
    if ("first" in expected) {
        expect(found.slice(0, 3)).toEqual(expected.first);
    }
});

test.each(plans)("makeItineraries gives each itinerary for $request a unique ID", ({ request }) => {
    const {
        origin,
        destination,
        date: _date,
        ...options
    } = request as Partial<PlanOptions> & {
        origin: LocationId;
        destination: LocationId;
        date: string;
    };

    const found = makeItineraries(origin, destination, { ...OPTIONS, ...options, date: DATE }, timetable, NOW);

    expect(new Set(found.map((itinerary) => itinerary.id)).size).toBe(found.length);
});

test("drive with no ferry starts at the current time of day", () => {
    expect(makeItineraries("hope", "TSA", OPTIONS, timetable, NOW)).toEqual([
        expect.objectContaining({
            route: "hope-TSA",
            depart: "2026-10-08T13:45:10",
            arrive: "2026-10-08T15:35:08",
            duration: 6598,
            steps: [
                {
                    kind: "MARK",
                    start: "2026-10-08T13:45:10",
                    end: "2026-10-08T13:45:10",
                    description: "Depart from Hope",
                },
                expect.objectContaining({ kind: "DRIVE", start: "2026-10-08T13:45:10", end: "2026-10-08T15:35:08" }),
                {
                    kind: "MARK",
                    start: "2026-10-08T15:35:08",
                    end: "2026-10-08T15:35:08",
                    description: "Arrive at Tsawwassen Terminal",
                },
            ],
        }),
    ]);
});

test("drive with no ferry keeps its ID across search times", () => {
    const [found] = makeItineraries("hope", "TSA", OPTIONS, timetable, NOW);
    const [later] = makeItineraries("hope", "TSA", OPTIONS, timetable, NOW + 60 * 1000);

    expect(found?.id).toBeDefined();
    expect(later?.id).toBe(found?.id);
    expect(later?.depart).not.toBe(found?.depart);
});

test("findRoutes finds a route through a link that is a dead end on another route", () => {
    // Earls Cove to Langdale leads nowhere on routes that already pass Horseshoe Bay or Tsawwassen.
    expect(findRoutes("SLT", "SWB").map((route) => route.join("-"))).toContain("SLT-ERL-LNG-HSB-TSA-SWB");
});

test.each(POPULAR_ROUTES)("findRoutes finds each way of the popular route from $from to $to", ({ from, to, ways }) => {
    const found = findRoutes(from, to).map((route) => route.join("-"));

    for (const way of ways) {
        // A sailing that departs from the terminal where the one before it arrived lists the terminal once.
        const stops = [from, ...way.flat(), to].filter((stop, index, all) => stop !== all[index - 1]);
        expect(found).toContain(stops.join("-"));
    }
});

const summarizeRoute = (origin: LocationId, destination: LocationId, options: Partial<PlanOptions>): string[] => {
    const date = options.date ?? DATE;
    return makeItineraries(origin, destination, { ...OPTIONS, ...options }, timetable, date - 24 * 60 * 60 * 1000)
        .filter((itinerary) => itinerary.route === `${origin}-TSA-${destination}`)
        .map(summarize);
};

test("makeItineraries continues overnight only if long is set", () => {
    const date = Date.UTC(2026, 9, 18);
    const overnight = "2026-10-18T22:00:00 > 2026-10-19T10:50:00 DUK-TSA-PSB [22:45 09:55]";

    expect(summarizeRoute("DUK", "PSB", { date })).not.toContain(overnight);
    expect(summarizeRoute("DUK", "PSB", { date, long: true })).toContain(overnight);
});

test("makeItineraries tries a later sailing if an earlier one with more stops arrives too late to connect", () => {
    // The 15:15 from Swartz Bay stops at three islands and arrives after check-in for the 19:30 closes.
    expect(summarizeRoute("SWB", "PSB", { date: Date.UTC(2026, 9, 21) })).toContain(
        "2026-10-21T16:15:00 > 2026-10-21T20:25:00 SWB-TSA-PSB [17:00 19:30]",
    );
});

test("makeItineraries returns no itineraries from a location to itself", () => {
    expect(makeItineraries("TSA", "TSA", OPTIONS, timetable, NOW)).toEqual([]);
});

const waitsFor = (options: Partial<PlanOptions>): string[] => {
    // Prince Rupert has its own check-in times for reservations and hostled vehicles.
    const itinerary = makeItineraries("PPR", "PSK", { ...OPTIONS, long: true, ...options }, timetable, DATE).find(
        (itinerary) => itinerary.route === "PPR-PSK",
    );
    return (itinerary?.steps ?? []).filter((step) => step.kind === "WAIT").map((step) => step.description);
};

test("check-in deadline is for hostled vehicles if selected, and for reservations by default", () => {
    expect(waitsFor({})).toEqual(["Arrive at Prince Rupert Terminal 15 minutes before booking check-in close"]);
    expect(waitsFor({ checkin: "hostled" })).toEqual([
        "Arrive at Prince Rupert Terminal 15 minutes before hostled vehicles check-in close",
    ]);
});
