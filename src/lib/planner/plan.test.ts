import { expect, test } from "vitest";
import { parseQuery, type Query } from "#lib/query.ts";
import { type FeedFiles, makeArchive } from "#test/feeds.ts";
import { parseFeed, Timetable } from "./gtfs";
import { itinerary, search } from "./plan";
import { terminalCoordinates } from "./schedule";
import { toLocal } from "./time";

const HSB_LNG = "from=HSB&to=LNG&date=2026-10-06";
/** The evening before in Vancouver. */
const EVENING_BEFORE = toLocal(Date.UTC(2026, 9, 6, 3));
/** Half past seven in Vancouver, when the only sailing of the day is under way. */
const UNDER_WAY = toLocal(Date.UTC(2026, 9, 6, 14, 30));
/** Noon in Vancouver, after the only sailing of the day. */
const NOON = toLocal(Date.UTC(2026, 9, 6, 19));

const timetableOf = (files?: FeedFiles): Timetable => {
    return new Timetable(parseFeed(makeArchive(files), terminalCoordinates()));
};

const queryOf = (query: string): Query => {
    return parseQuery(new URLSearchParams(query), "2026-10-06");
};

test("search has the itineraries worth taking from the feed", () => {
    expect(search(queryOf(HSB_LNG), timetableOf(), EVENING_BEFORE)).toEqual({
        origin: "HSB",
        destination: "LNG",
        date: "2026-10-06",
        covered: true,
        itineraries: [
            expect.objectContaining({
                // Check-in for booked vehicles closes 30 minutes before the sailing at 07:30, and 15 minutes early.
                depart: "2026-10-06T06:45:00",
                arrive: "2026-10-06T08:10:00",
                duration: 85 * 60,
            }),
        ],
        moreRoutes: 0,
        departed: 0,
        underway: 0,
        now: "2026-10-05T20:00:00",
    });
});

test("search leaves out what has already left", () => {
    expect(search(queryOf(HSB_LNG), timetableOf(), NOON)).toMatchObject({ itineraries: [], departed: 1 });
});

test("search says when the feed does not cover the date", () => {
    const timetable = timetableOf({ feedInfo: "Publisher,20260101,20261005" });

    expect(search(queryOf(HSB_LNG), timetable, EVENING_BEFORE)).toMatchObject({ covered: false, itineraries: [] });
});

test("search is made with the check-in and the time to arrive early that are asked for", () => {
    const found = search(queryOf(`${HSB_LNG}&early=30&checkin=assured`), timetableOf(), EVENING_BEFORE);

    // Assured loading closes 20 minutes before the sailing at 07:30.
    expect(found?.itineraries[0]?.depart).toBe("2026-10-06T06:40:00");
});

test("search shows the trips under way when asked to", () => {
    const without = search(queryOf(HSB_LNG), timetableOf(), UNDER_WAY);
    const found = search(queryOf(`${HSB_LNG}&underway=1&sort=arrival`), timetableOf(), UNDER_WAY);

    expect(without).toMatchObject({ itineraries: [], departed: 1, underway: 1 });
    expect(found).toMatchObject({ itineraries: [{ depart: "2026-10-06T06:45:00" }], departed: 0, underway: 0 });
});

test.each([
    ["from a place that is not known", "from=ATLANTIS&to=LNG"],
    // Every object has something by this name.
    ["to a place that is not known", "from=HSB&to=toString"],
    ["without a place to go to", "from=HSB"],
    ["from a place to itself", "from=HSB&to=HSB"],
])("no search %s", (_, query) => {
    expect(search(queryOf(query), timetableOf(), EVENING_BEFORE)).toBeUndefined();
});

test("itinerary of a search is found by its ID, even after it has left", () => {
    const [found] = search(queryOf(HSB_LNG), timetableOf(), EVENING_BEFORE)?.itineraries ?? [];

    expect(found).toBeDefined();
    expect(itinerary(queryOf(HSB_LNG), found?.id ?? "", timetableOf(), NOON)).toEqual(found);
});

test.each([
    ["by an ID that none has", HSB_LNG, "00000000000"],
    ["without an ID", HSB_LNG, ""],
    ["of a search that cannot be made", "from=HSB&to=ATLANTIS", "00000000000"],
])("no itinerary is found %s", (_, query, id) => {
    expect(itinerary(queryOf(query), id, timetableOf(), EVENING_BEFORE)).toBeUndefined();
});
