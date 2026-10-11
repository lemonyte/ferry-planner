import { expect, test } from "vitest";

import {
    addDays,
    daysBetween,
    formatDay,
    formatDistance,
    formatDuration,
    formatTime,
    secondsBetween,
} from "./format.ts";

test("formatTime uses a 12-hour clock and omits seconds", () => {
    expect(formatTime("2026-10-08T06:20:50")).toBe("6:20 am");
    expect(formatTime("2026-10-08T13:34:24")).toBe("1:34 pm");
});

test("formatTime shows midnight and noon as 12", () => {
    expect(formatTime("2026-10-08T00:05:00")).toBe("12:05 am");
    expect(formatTime("2026-10-08T12:00:00")).toBe("12:00 pm");
});

test("formatDay abbreviates the weekday and month", () => {
    expect(formatDay("2026-10-09")).toBe("Fri, Oct 9");
    expect(formatDay("2027-01-01T05:00:00")).toBe("Fri, Jan 1");
});

test("formatDuration uses hours and minutes", () => {
    expect(formatDuration(26014)).toBe("7 h 14 min");
    expect(formatDuration(3 * 3600)).toBe("3 h");
});

test("formatDuration uses only minutes below one hour", () => {
    expect(formatDuration(45 * 60)).toBe("45 min");
    expect(formatDuration(20)).toBe("0 min");
});

test("formatDistance rounds to whole kilometers", () => {
    expect(formatDistance(144.42090000000002)).toBe("144 km");
});

test("secondsBetween counts across midnight", () => {
    expect(secondsBetween("2026-10-08T23:30:00", "2026-10-09T00:44:00")).toBe(74 * 60);
});

test("daysBetween counts midnights, regardless of the time between", () => {
    expect(daysBetween("2026-10-08T06:00:00", "2026-10-08T23:59:00")).toBe(0);
    expect(daysBetween("2026-10-08T23:30:00", "2026-10-09T00:44:00")).toBe(1);
});

test("addDays crosses the end of a month", () => {
    expect(addDays("2026-10-31", 1)).toBe("2026-11-01");
    expect(addDays("2026-10-08", 0)).toBe("2026-10-08");
});
