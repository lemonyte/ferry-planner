import { expect, test } from "vitest";
import { digest } from "#test/digest.ts";
import plans from "#test/fixtures/plans.json";
import routes from "#test/fixtures/routes.json";
import { makeTimetable } from "#test/fixtures.ts";
import type { LocationId } from "./data/locations";
import { findRoutes, type PlanOptions, routePlans } from "./route";
import { parseLocal } from "./time";

const timetable = makeTimetable();
const DATE = Date.UTC(2026, 9, 8);
const NOW = Date.UTC(2026, 9, 8, 13, 45, 10);
const OPTIONS: PlanOptions = { date: DATE, showAll: false, assured: false, hostled: false, buffer: 15 };

test.each(Object.entries(routes))("routes for %s are as expected", (id, expected) => {
    const [origin, destination] = id.split("-") as [LocationId, LocationId];

    const found = findRoutes(origin, destination);

    expect(found).toHaveLength(expected.count);
    if ("routes" in expected) {
        expect(found).toEqual(expected.routes);
    }
    expect(digest(found)).toBe(expected.digest);
});

test.each(plans)("route plans for $request are as expected", (expected) => {
    const { origin, destination, date, ...request } = expected.request as {
        origin: LocationId;
        destination: LocationId;
        date: string;
        show_all?: boolean;
        assured?: boolean;
        hostled?: boolean;
        buffer?: number;
    };

    const found = routePlans(
        origin,
        destination,
        {
            date: parseLocal(date) ?? Number.NaN,
            showAll: request.show_all ?? false,
            assured: request.assured ?? false,
            hostled: request.hostled ?? false,
            buffer: request.buffer ?? 15,
        },
        timetable,
        NOW,
    );

    expect(found.map((plan) => plan.hash)).toEqual(expected.ids);
    expect(new Set(expected.ids).size).toBe(expected.count);
    if ("first" in expected) {
        expect(found.slice(0, 3)).toEqual(expected.first);
    }
    expect(digest(found)).toBe(expected.digest);
});

test("route plans are ordered by duration", () => {
    const durations = routePlans("TSA", "PST", OPTIONS, timetable, NOW).map((plan) => plan.duration);

    expect(durations).toEqual(durations.toSorted((a, b) => a - b));
});

test("drive without a sailing starts at the current time of day", () => {
    expect(routePlans("hope", "TSA", OPTIONS, timetable, NOW)).toEqual([
        expect.objectContaining({
            depart_time: "2026-10-08T13:45:10",
            arrive_time: "2026-10-08T15:35:08",
            duration: 6598,
            driving_duration: 6598,
            segments: [
                {
                    connection: expect.objectContaining({ id: "hope-TSA", type: "CAR" }),
                    times: [
                        {
                            start: "2026-10-08T13:45:10",
                            end: "2026-10-08T13:45:10",
                            description: "Depart from Hope",
                            type: "TRAVEL",
                        },
                        expect.objectContaining({
                            start: "2026-10-08T13:45:10",
                            end: "2026-10-08T15:35:08",
                            type: "TRAVEL",
                        }),
                        {
                            start: "2026-10-08T15:35:08",
                            end: "2026-10-08T15:35:08",
                            description: "Arrive at Tsawwassen Terminal",
                            type: "TRAVEL",
                        },
                    ],
                },
            ],
        }),
    ]);
});

test("no route plans between a location and itself", () => {
    expect(routePlans("TSA", "TSA", OPTIONS, timetable, NOW)).toEqual([]);
});

const waitsFor = (options: Partial<PlanOptions>): string[] => {
    // Prince Rupert has check-in times of its own for reservations and for hostled vehicles.
    const plan = routePlans("PPR", "PSK", { ...OPTIONS, showAll: true, ...options }, timetable, DATE).find(
        (plan) => plan.segments.length === 1,
    );
    return (plan?.segments ?? []).flatMap((segment) =>
        segment.times.filter((time) => time.type === "WAIT").map((time) => time.description),
    );
};

test("check-in closes for hostled vehicles when they are asked for, and for reservations otherwise", () => {
    expect(waitsFor({})).toEqual(["Arrive at Prince Rupert Terminal 15 minutes before booking check-in close"]);
    expect(waitsFor({ hostled: true })).toEqual([
        "Arrive at Prince Rupert Terminal 15 minutes before hostled vehicles check-in close",
    ]);
});
