// Writes the planner results that the tests compare against, using the feed in `test/fixtures`.
//
// Run with `bun test/export-fixtures.ts` after a change that intentionally changes the results,
// and review the diff before committing.

import { writeFileSync } from "node:fs";

import type { LocationId, TerminalId } from "#lib/planner/data/locations.ts";
import { findRoutes, makeItineraries, type PlanOptions } from "#lib/planner/route.ts";
import { getSchedule } from "#lib/planner/schedule.ts";
import { parseLocal } from "#lib/planner/time.ts";

import { makeTimetable } from "./fixtures.ts";
import { summarize } from "./summary.ts";

const FIXTURES = new URL("./fixtures/", import.meta.url);
const DATE = "2026-10-08";
/** Current local time for the itineraries, the same as in the tests. */
const NOW = Date.UTC(2026, 9, 8, 13, 45, 10);
/** Longest list stored in full. Longer lists are stored as a count only. */
const MAX_LISTED = 200;
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

interface PlanRequest extends Partial<Omit<PlanOptions, "date">> {
    origin: LocationId;
    destination: LocationId;
}

const PLANS: PlanRequest[] = [
    { origin: "HSB", destination: "NAN" },
    { origin: "TSA", destination: "PST" },
    { origin: "TSA", destination: "PLH", long: true },
    { origin: "LNG", destination: "PVB" },
    { origin: "CMX", destination: "TEX", long: true },
    { origin: "vancouver", destination: "victoria" },
    { origin: "vancouver", destination: "victoria", checkin: "assured", early: 30 },
    { origin: "vancouver", destination: "victoria", checkin: "hostled", early: 0 },
    { origin: "nanaimo", destination: "gibsons", long: true },
    { origin: "tlell", destination: "west_vancouver", long: true },
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

const timetable = makeTimetable();

/** Store the count of a list, and the list itself if it is short enough to review. */
const list = (items: string[]): { count: number; listed?: string[] } => {
    return { count: items.length, ...(items.length <= MAX_LISTED ? { listed: items } : {}) };
};

const routes = Object.fromEntries(
    ROUTES.map(([origin, destination]) => [
        `${origin}-${destination}`,
        list(findRoutes(origin, destination).map((route) => route.join("-"))),
    ]),
);

const plans = PLANS.map(({ origin, destination, ...options }, index) => {
    const found = makeItineraries(
        origin,
        destination,
        { date: toTime(DATE), checkin: "reservation", early: 15, long: false, ...options },
        timetable,
        NOW,
    );
    return {
        request: { origin, destination, date: DATE, ...options },
        ...list(found.map(summarize)),
        // A few full itineraries show the structure of the rest.
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
