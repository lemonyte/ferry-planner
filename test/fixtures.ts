import { parseFeed, Timetable } from "#lib/planner/gtfs.ts";
import { terminalCoordinates } from "#lib/planner/schedule.ts";
import feedUrl from "./fixtures/feed.zip?inline";

/** The BC Ferries feed as of 2026-09-27, which the expected results in `test/fixtures` were made with. */
export const FEED = Uint8Array.from(atob(feedUrl.slice(feedUrl.indexOf(",") + 1)), (character) =>
    character.charCodeAt(0),
);

export const makeTimetable = (): Timetable => {
    return new Timetable(parseFeed(FEED, terminalCoordinates()));
};
