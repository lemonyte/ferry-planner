import { readFileSync } from "node:fs";

import { parseFeed, Timetable } from "#lib/planner/gtfs.ts";
import { terminalCoordinates } from "#lib/planner/schedule.ts";

/** The BC Ferries feed as of 2026-09-27, from which the expected results in `test/fixtures` were generated. */
const FEED: Uint8Array = readFileSync(new URL("./fixtures/feed.zip", import.meta.url));

export const makeTimetable = (): Timetable => {
    return new Timetable(parseFeed(FEED, terminalCoordinates()));
};
