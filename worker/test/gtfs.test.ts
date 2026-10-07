import { expect, test } from "vitest";
import { parseFeed, type Sailing, Timetable } from "../src/gtfs";
import { EVERY_DAY, type FeedFiles, HSB_TO_LNG, LOCATIONS, makeArchive, STOP_TIMES_COLUMNS, STOPS } from "./feeds";

// Tuesday.
const DATE = Date.UTC(2026, 9, 6);

const makeTimetable = (files: FeedFiles = {}): Timetable => {
    return new Timetable(parseFeed(makeArchive(files), LOCATIONS));
};

const at = (day: number, hour: number, minute: number): number => {
    return Date.UTC(2026, 9, day, hour, minute);
};

const sailing = (departure: number, arrival: number, stops: string[] = []): Sailing => {
    return { departure, arrival, stops };
};

test("sailing between two locations on a day the service runs", () => {
    const timetable = makeTimetable({ stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
});

test("sailings are only worked out once for the same locations and date", () => {
    const timetable = makeTimetable({ stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toBe(timetable.sailings("HSB", "LNG", DATE));
});

test("no sailings on a weekday the service does not run", () => {
    const timetable = makeTimetable({ calendar: "daily,1,0,1,1,1,1,1,20260101,20261231", stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
});

test("no sailings outside the service date range", () => {
    const timetable = makeTimetable({ calendar: "daily,1,1,1,1,1,1,1,20261007,20261231", stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
});

test("no sailings on a date removed from the service", () => {
    const timetable = makeTimetable({ calendarDates: "daily,20261006,2\n", stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
});

test("sailings on a date added to the service", () => {
    const timetable = makeTimetable({
        calendar: "daily,0,0,0,0,0,0,0,20000101,20500101",
        calendarDates: "daily,20261006,1\n",
        stopTimes: HSB_TO_LNG,
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
    expect(timetable.sailings("HSB", "LNG", Date.UTC(2026, 9, 7))).toEqual([]);
});

test("sailing past midnight departs on the day after its service day", () => {
    const timetable = makeTimetable({ stopTimes: "t,25:10:00,25:10:00,1,1\nt,25:50:00,25:50:00,2,2\n" });

    expect(timetable.sailings("HSB", "LNG", DATE)[0]).toEqual(sailing(at(6, 1, 10), at(6, 1, 50)));
});

test("sailing past midnight does not depart before its service starts", () => {
    const timetable = makeTimetable({
        calendar: "daily,1,1,1,1,1,1,1,20261006,20261231",
        stopTimes: "t,25:10:00,25:10:00,1,1\nt,25:50:00,25:50:00,2,2\n",
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
    expect(timetable.sailings("HSB", "LNG", Date.UTC(2026, 9, 7))).toEqual([sailing(at(7, 1, 10), at(7, 1, 50))]);
});

test("sailing arriving past midnight arrives on the next day", () => {
    const timetable = makeTimetable({ stopTimes: "t,23:30:00,23:30:00,1,1\nt,24:15:00,24:15:00,2,2\n" });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 23, 30), at(7, 0, 15))]);
});

test("sailings are ordered by departure", () => {
    const timetable = makeTimetable({
        trips: "r,daily,late\nr,daily,early\n",
        stopTimes:
            "late,17:00:00,17:00:00,1,1\nlate,17:40:00,17:40:00,2,2\n" +
            "early,07:30:00,07:30:00,1,1\nearly,08:10:00,08:10:00,2,2\n",
    });

    expect(timetable.sailings("HSB", "LNG", DATE).map((sailing) => sailing.departure)).toEqual([
        at(6, 7, 30),
        at(6, 17, 0),
    ]);
});

test("same sailing on two services is returned once", () => {
    const timetable = makeTimetable({
        calendar: `${EVERY_DAY}\nholiday,1,1,1,1,1,1,1,20260101,20261231`,
        trips: "r,daily,t\nr,holiday,u\n",
        stopTimes: HSB_TO_LNG + HSB_TO_LNG.replaceAll("t,", "u,"),
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
});

const THREE_STOPS = "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:25:00,2,2\nt,10:00:00,10:00:00,3,3\n";

test("sailing with a stop on the way runs between every pair of its stops", () => {
    const timetable = makeTimetable({ stopTimes: THREE_STOPS });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 10, 0), ["LNG"])]);
    expect(timetable.sailings("LNG", "NAN", DATE)).toEqual([sailing(at(6, 8, 25), at(6, 10, 0))]);
});

test("sailing does not run against the order of its stops", () => {
    const timetable = makeTimetable({ stopTimes: THREE_STOPS });

    expect(timetable.sailings("NAN", "HSB", DATE)).toEqual([]);
});

test("sailing ends at its first call at the destination", () => {
    const timetable = makeTimetable({
        stopTimes:
            "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:20:00,2,2\nt,09:00:00,09:10:00,1,3\nt,09:50:00,09:50:00,2,4\n",
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([
        sailing(at(6, 7, 30), at(6, 8, 10)),
        sailing(at(6, 9, 10), at(6, 9, 50)),
    ]);
});

test("sailing departs at its last call at the origin", () => {
    const timetable = makeTimetable({
        stopTimes:
            "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:20:00,2,2\nt,09:00:00,09:10:00,1,3\nt,10:50:00,10:50:00,3,4\n",
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 9, 10), at(6, 10, 50))]);
});

test("sailing does not continue on an earlier part of its trip", () => {
    const timetable = makeTimetable({
        stopTimes:
            "t,07:00:00,07:00:00,2,1\nt,08:00:00,08:10:00,3,2\nt,09:00:00,09:10:00,1,3\nt,09:50:00,09:50:00,2,4\n",
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([]);
});

test("stop far from every location is ignored", () => {
    // The second stop is about 1 km from Langdale, the nearest location.
    const timetable = makeTimetable({
        stops: STOPS.replace("2,Langdale,49.4341,-123.4721", "2,Langdale Heights,49.4430,-123.4720"),
        stopTimes: HSB_TO_LNG,
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
});

test("stop without coordinates is ignored", () => {
    const timetable = makeTimetable({
        stops: `${STOPS}4,Somewhere,,\n`,
        stopTimes: `${HSB_TO_LNG}t,09:00:00,09:00:00,4,3\n`,
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
});

test("stop without times is passed through", () => {
    const timetable = makeTimetable({ stopTimes: "t,07:30:00,07:30:00,1,1\nt,,,2,2\nt,10:00:00,10:00:00,3,3\n" });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 10, 0))]);
});

test("stop with only one time arrives and departs at it", () => {
    const timetable = makeTimetable({ stopTimes: "t,,07:30:00,1,1\nt,08:10:00,,2,2\nt,10:00:00,,3,3\n" });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
    expect(timetable.sailings("LNG", "NAN", DATE)).toEqual([sailing(at(6, 8, 10), at(6, 10, 0))]);
});

test("feed without a calendar runs services on their added dates", () => {
    const timetable = makeTimetable({ calendar: null, calendarDates: "daily,20261006,1\n", stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
    expect(timetable.sailings("HSB", "LNG", Date.UTC(2026, 9, 7))).toEqual([]);
});

test("feed without calendar dates runs services on their calendar", () => {
    const timetable = makeTimetable({ calendarDates: null, stopTimes: HSB_TO_LNG });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
});

test("feed lists the locations without sailings", () => {
    expect(parseFeed(makeArchive({ stopTimes: HSB_TO_LNG }), LOCATIONS).unserved).toEqual(["NAN"]);
});

test("feed that is not a GTFS archive is rejected", () => {
    expect(() => parseFeed(new TextEncoder().encode("<html>Waiting room</html>"), LOCATIONS)).toThrow();
});

test("feed with a row that is missing a number is rejected", () => {
    // The stop sequences are missing.
    const archive = makeArchive({ stopTimes: "t,07:30:00,07:30:00,1\nt,08:10:00,08:10:00,2\n" });

    expect(() => parseFeed(archive, LOCATIONS)).toThrow();
});

test("feed with a quoted value is read without its quotes", () => {
    const trip = '"t ""express"", 1"';
    const archive = makeArchive({ trips: `r,daily,${trip}\n`, stopTimes: HSB_TO_LNG.replaceAll("t,", `${trip},`) });

    expect(parseFeed(archive, LOCATIONS).legs.map((leg) => leg.trip)).toEqual(['t "express", 1']);
});

const PICKUP_COLUMNS = `${STOP_TIMES_COLUMNS},pickup_type,drop_off_type`;

test("no sailing from a stop that cannot be boarded at", () => {
    const timetable = makeTimetable({
        stopTimesColumns: PICKUP_COLUMNS,
        stopTimes: "t,07:30:00,07:30:00,1,1,1,0\nt,08:10:00,08:10:00,2,2,0,0\n",
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
});

test("no sailing to a stop that cannot be alighted at", () => {
    const timetable = makeTimetable({
        stopTimesColumns: PICKUP_COLUMNS,
        stopTimes: "t,07:30:00,07:30:00,1,1,0,0\nt,08:10:00,08:10:00,2,2,0,1\n",
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([]);
});

test("feed covers dates in its date range", () => {
    const timetable = makeTimetable({ stopTimes: HSB_TO_LNG, feedInfo: "Publisher,20260926,20261006" });

    expect(timetable.covers(Date.UTC(2026, 8, 26))).toBe(true);
    expect(timetable.covers(DATE)).toBe(true);
});

test("feed does not cover dates outside its date range", () => {
    const timetable = makeTimetable({ stopTimes: HSB_TO_LNG, feedInfo: "Publisher,20260926,20261006" });

    expect(timetable.covers(Date.UTC(2026, 8, 25))).toBe(false);
    expect(timetable.covers(Date.UTC(2026, 9, 7))).toBe(false);
});

test("feed without a date range covers every date", () => {
    expect(makeTimetable({ stopTimes: HSB_TO_LNG }).covers(DATE)).toBe(true);
    expect(makeTimetable({ stopTimes: HSB_TO_LNG, feedInfo: "Publisher,," }).covers(DATE)).toBe(true);
});

// The BC Ferries feed lists the dates that a single trip is added to or removed from
// under a service named after both the trip's service and the trip.
const EXCEPTION_ONLY = "daily,0,0,0,0,0,0,0,20000101,20500101";
const EARLY_AND_LATE = {
    trips: "r,daily,early\nr,daily,late\n",
    stopTimes: `${HSB_TO_LNG.replaceAll("t,", "early,")}late,17:00:00,17:00:00,1,1\nlate,17:40:00,17:40:00,2,2\n`,
};

test("sailing runs on a date added for its trip only", () => {
    const timetable = makeTimetable({
        calendar: EXCEPTION_ONLY,
        calendarDates: "dailyearly,20261006,1\n",
        ...EARLY_AND_LATE,
    });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 8, 10))]);
});

test("sailing does not run on a date removed for its trip only", () => {
    const timetable = makeTimetable({ calendarDates: "dailyearly,20261006,2\n", ...EARLY_AND_LATE });

    expect(timetable.sailings("HSB", "LNG", DATE)).toEqual([sailing(at(6, 17, 0), at(6, 17, 40))]);
});

// The BC Ferries feed lists each part of a sailing that calls at several terminals as a trip of its own.
const TRIPS = "r,daily,a\nr,daily,b\nr,daily,c\n";
const HSB_TO_LNG_BY_8_10 = "a,07:30:00,07:30:00,1,1\na,08:10:00,08:10:00,2,2\n";
const LNG_TO_NAN_AT_8_25 = "b,08:25:00,08:25:00,2,1\nb,10:00:00,10:00:00,3,2\n";

test("sailing continues on the trip that departs from where it arrives", () => {
    const timetable = makeTimetable({ trips: TRIPS, stopTimes: HSB_TO_LNG_BY_8_10 + LNG_TO_NAN_AT_8_25 });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 10, 0), ["LNG"])]);
});

test("sailing continues on the first trip to arrive", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: `${HSB_TO_LNG_BY_8_10}c,08:15:00,08:15:00,2,1\nc,10:30:00,10:30:00,3,2\n${LNG_TO_NAN_AT_8_25}`,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 10, 0), ["LNG"])]);
});

test("sailing does not continue on a trip that departs before it arrives", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: `${HSB_TO_LNG_BY_8_10}b,08:05:00,08:05:00,2,1\nb,10:00:00,10:00:00,3,2\n`,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([]);
});

test("sailing does not continue on a trip that departs hours after it arrives", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: `${HSB_TO_LNG_BY_8_10}b,10:15:00,10:15:00,2,1\nb,12:00:00,12:00:00,3,2\n`,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([]);
});

test("sailing continues past midnight", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes:
            "a,23:30:00,23:30:00,1,1\na,24:15:00,24:15:00,2,2\nb,24:30:00,24:30:00,2,1\nb,25:30:00,25:30:00,3,2\n",
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 23, 30), at(7, 1, 30), ["LNG"])]);
    expect(timetable.sailings("LNG", "NAN", Date.UTC(2026, 9, 7))).toEqual([sailing(at(7, 0, 30), at(7, 1, 30))]);
});

test("sailing with a transfer is left out when a later sailing arrives no later", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: `${HSB_TO_LNG_BY_8_10}${LNG_TO_NAN_AT_8_25}c,08:00:00,08:00:00,1,1\nc,09:40:00,09:40:00,3,2\n`,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 8, 0), at(6, 9, 40))]);
});

test("sailing without a transfer is kept when a later sailing arrives earlier", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: `${HSB_TO_LNG_BY_8_10}${LNG_TO_NAN_AT_8_25}c,07:00:00,07:00:00,1,1\nc,11:00:00,11:00:00,3,2\n`,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([
        sailing(at(6, 7, 0), at(6, 11, 0)),
        sailing(at(6, 7, 30), at(6, 10, 0), ["LNG"]),
    ]);
});

// Transfers at Langdale take at least 45 minutes.
const LNG_TRANSFER = "2,2,2,2700\n";

test("sailing does not continue on a trip that departs within the minimum transfer time", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: HSB_TO_LNG_BY_8_10 + LNG_TO_NAN_AT_8_25,
        transfers: LNG_TRANSFER,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([]);
});

test("sailing continues on a trip that departs after the minimum transfer time", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimes: `${HSB_TO_LNG_BY_8_10}b,08:55:00,08:55:00,2,1\nb,10:30:00,10:30:00,3,2\n`,
        transfers: LNG_TRANSFER,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 10, 30), ["LNG"])]);
});

test("sailing stays on its trip without waiting for the minimum transfer time", () => {
    const timetable = makeTimetable({ stopTimes: THREE_STOPS, transfers: LNG_TRANSFER });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([sailing(at(6, 7, 30), at(6, 10, 0), ["LNG"])]);
});

test("sailing does not continue from a stop that cannot be alighted at", () => {
    const timetable = makeTimetable({
        trips: TRIPS,
        stopTimesColumns: PICKUP_COLUMNS,
        stopTimes: `a,07:30:00,07:30:00,1,1,0,0\na,08:10:00,08:10:00,2,2,0,1\n${LNG_TO_NAN_AT_8_25}`,
    });

    expect(timetable.sailings("HSB", "NAN", DATE)).toEqual([]);
});
