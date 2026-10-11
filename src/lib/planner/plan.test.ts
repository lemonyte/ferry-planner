import { expect, test } from "vitest";

import { parseQuery, type Query } from "#lib/query.ts";
import { type FeedFiles, makeArchive } from "#test/feeds.ts";

import { parseFeed, Timetable } from "./gtfs.ts";
import { itinerary, search } from "./plan.ts";
import { terminalCoordinates } from "./schedule.ts";
import { toLocal } from "./time.ts";

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

test("search returns the itineraries from the feed", () => {
    expect(search(queryOf(HSB_LNG), timetableOf(), EVENING_BEFORE)).toEqual({
        covered: true,
        itineraries: [
            expect.objectContaining({
                // Booked check-in closes 30 minutes before the 07:30 sailing, plus 15 minutes early.
                depart: "2026-10-06T06:45:00",
                arrive: "2026-10-06T08:10:00",
                duration: 85 * 60,
            }),
        ],
        more: 0,
        departed: 0,
        underway: 0,
        now: "2026-10-05T20:00:00",
    });
});

test("search excludes departed itineraries", () => {
    expect(search(queryOf(HSB_LNG), timetableOf(), NOON)).toMatchObject({ itineraries: [], departed: 1 });
});

test("search reports if the feed does not cover the date", () => {
    const timetable = timetableOf({ feedInfo: "Publisher,20260101,20261005" });

    expect(search(queryOf(HSB_LNG), timetable, EVENING_BEFORE)).toMatchObject({ covered: false, itineraries: [] });
});

test("search uses the selected check-in type and early arrival", () => {
    const found = search(queryOf(`${HSB_LNG}&early=30&checkin=assured`), timetableOf(), EVENING_BEFORE);

    // Assured loading closes 20 minutes before the 07:30 sailing.
    expect(found?.itineraries[0]?.depart).toBe("2026-10-06T06:40:00");
});

test("search includes itineraries under way if underway is set", () => {
    const without = search(queryOf(HSB_LNG), timetableOf(), UNDER_WAY);
    const found = search(queryOf(`${HSB_LNG}&underway=1&sort=arrival`), timetableOf(), UNDER_WAY);

    expect(without).toMatchObject({ itineraries: [], departed: 1, underway: 1 });
    expect(found).toMatchObject({ itineraries: [{ depart: "2026-10-06T06:45:00" }], departed: 0, underway: 0 });
});

test.each([
    ["from an unknown place", "from=ATLANTIS&to=LNG"],
    // An inherited `Object` property.
    ["to an unknown place", "from=HSB&to=toString"],
    ["without a destination", "from=HSB"],
    ["from a place to itself", "from=HSB&to=HSB"],
])("search returns undefined %s", (_, query) => {
    expect(search(queryOf(query), timetableOf(), EVENING_BEFORE)).toBeUndefined();
});

test("itinerary is found by ID after it has departed", () => {
    const [found] = search(queryOf(HSB_LNG), timetableOf(), EVENING_BEFORE)?.itineraries ?? [];

    expect(found).toBeDefined();
    expect(itinerary(queryOf(HSB_LNG), found?.id ?? "", timetableOf(), NOON)).toEqual(found);
});

test.each([
    ["for an unknown ID", HSB_LNG, "00000000000"],
    ["without an ID", HSB_LNG, ""],
    ["for an invalid search", "from=HSB&to=ATLANTIS", "00000000000"],
])("itinerary returns undefined %s", (_, query, id) => {
    expect(itinerary(queryOf(query), id, timetableOf(), EVENING_BEFORE)).toBeUndefined();
});

test("drive with no ferry is found by ID at a later time", () => {
    const drive = queryOf("from=hope&to=TSA&date=2026-10-06");
    const [found] = search(drive, timetableOf(), EVENING_BEFORE)?.itineraries ?? [];

    expect(found).toBeDefined();
    expect(itinerary(drive, found?.id ?? "", timetableOf(), NOON)).toMatchObject({ id: found?.id, route: "hope-TSA" });
});
