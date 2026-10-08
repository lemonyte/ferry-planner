import { createHash } from "node:crypto";
import { parseFeed, Timetable } from "#lib/planner/gtfs.ts";
import { terminalCoordinates } from "#lib/planner/schedule.ts";
import feedUrl from "./fixtures/feed.zip?inline";

/** The BC Ferries feed as of 2026-09-27, which the fixtures exported from the Python planner were made with. */
export const FEED = Uint8Array.from(atob(feedUrl.slice(feedUrl.indexOf(",") + 1)), (character) =>
    character.charCodeAt(0),
);

export const makeTimetable = (): Timetable => {
    return new Timetable(parseFeed(FEED, terminalCoordinates()));
};

const sortKeys = (value: unknown): unknown => {
    if (Array.isArray(value)) {
        return value.map(sortKeys);
    }
    if (value && typeof value === "object") {
        return Object.fromEntries(
            Object.entries(value)
                .filter(([, item]) => item !== undefined)
                .sort(([a], [b]) => (a < b ? -1 : 1))
                .map(([key, item]) => [key, sortKeys(item)]),
        );
    }
    return value;
};

/** Hash a value the same way as `tests/export_worker_fixtures.py`. */
export const digest = (value: unknown): string => {
    return createHash("sha256")
        .update(JSON.stringify(sortKeys(value)))
        .digest("hex");
};
