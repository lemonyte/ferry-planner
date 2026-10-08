// Writes the results of the planner that the tests compare it against, from the feed in `test/fixtures`.
//
// Run with `bun test/export-fixtures.ts` after a change that is meant to change the results,
// and look over what has changed in them before keeping it.

import { readFileSync, writeFileSync } from "node:fs";
import type { LocationId, TerminalId } from "#lib/planner/data/locations.ts";
import { parseFeed, Timetable } from "#lib/planner/gtfs.ts";
import { findRoutes, routePlans } from "#lib/planner/route.ts";
import { getSchedule, terminalCoordinates } from "#lib/planner/schedule.ts";
import { parseLocal } from "#lib/planner/time.ts";
import { digest } from "./digest.ts";

const FIXTURES = new URL("./fixtures/", import.meta.url);
const DATE = "2026-10-08";
/** Current local time that the route plans are made at, the same as in the tests. */
const NOW = Date.UTC(2026, 9, 8, 13, 45, 10);
/** Longest list of routes kept whole, as longer ones are only kept as a digest. */
const MAX_ROUTES = 25;
const ROUTES: [LocationId, LocationId][] = [
    ["TSA", "PST"],
    ["LNG", "PVB"],
    ["HSB", "NAN"],
    ["vancouver", "victoria"],
    ["smithers", "tofino"],
    ["prince_rupert", "victoria"],
    ["100_mile_house", "MIL"],
    ["atlin", "port_moody"],
    ["hope", "TSA"],
    ["tlell", "west_vancouver"],
    ["CHM", "nimpo_lake"],
    ["NAH", "gibsons"],
    ["port_hardy", "tsawwassen"],
    ["sandspit_village", "houston"],
];

interface PlanRequest {
    origin: LocationId;
    destination: LocationId;
    show_all?: boolean;
    assured?: boolean;
    hostled?: boolean;
    buffer?: number;
}

const PLANS: PlanRequest[] = [
    { origin: "HSB", destination: "NAN" },
    { origin: "TSA", destination: "PST" },
    { origin: "TSA", destination: "PLH", show_all: true },
    { origin: "LNG", destination: "PVB" },
    { origin: "CMX", destination: "TEX", show_all: true },
    { origin: "vancouver", destination: "victoria" },
    { origin: "vancouver", destination: "victoria", assured: true, buffer: 30 },
    { origin: "vancouver", destination: "victoria", hostled: true, buffer: 0 },
    { origin: "nanaimo", destination: "gibsons", show_all: true },
    { origin: "tlell", destination: "west_vancouver", show_all: true },
    { origin: "port_hardy", destination: "tsawwassen" },
];
const SCHEDULES: { origin: TerminalId; destination: TerminalId; date: string }[] = [
    { origin: "HSB", destination: "NAN", date: DATE },
    { origin: "TSA", destination: "PST", date: DATE },
    { origin: "PPR", destination: "PPH", date: DATE },
    { origin: "HSB", destination: "NAN", date: "2027-06-01" },
];

const toTime = (date: string): number => {
    const time = parseLocal(date);
    if (time === undefined) {
        throw new Error(`${date} is not a date`);
    }
    return time;
};

const timetable = new Timetable(parseFeed(readFileSync(new URL("feed.zip", FIXTURES)), terminalCoordinates()));

const routes = Object.fromEntries(
    ROUTES.map(([origin, destination]) => {
        const found = findRoutes(origin, destination);
        return [
            `${origin}-${destination}`,
            { count: found.length, digest: digest(found), ...(found.length <= MAX_ROUTES ? { routes: found } : {}) },
        ];
    }),
);

const plans = PLANS.map((request, index) => {
    const found = routePlans(
        request.origin,
        request.destination,
        {
            date: toTime(DATE),
            showAll: request.show_all ?? false,
            assured: request.assured ?? false,
            hostled: request.hostled ?? false,
            buffer: request.buffer ?? 15,
        },
        timetable,
        NOW,
    );
    return {
        request: { date: DATE, ...request },
        count: found.length,
        digest: digest(found),
        ids: found.map((plan) => plan.hash),
        // A few whole plans show the shape of the others.
        ...(index === 0 ? { first: found.slice(0, 3) } : {}),
    };
});

const schedules = SCHEDULES.map((request) => ({
    request,
    response: getSchedule(timetable, request.origin, request.destination, toTime(request.date)),
}));

for (const [name, value] of Object.entries({ routes, plans, schedules })) {
    writeFileSync(new URL(`${name}.json`, FIXTURES), `${JSON.stringify(value, null, 1)}\n`);
    console.log(name, Object.keys(value).length);
}
