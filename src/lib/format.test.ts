import { expect, test } from "vitest";
import { addDays, daysBetween, formatDay, formatDistance, formatDuration, formatTime, secondsBetween } from "./format";

test("time is on a twelve-hour clock, without its seconds", () => {
    expect(formatTime("2026-10-08T06:20:50")).toBe("6:20 am");
    expect(formatTime("2026-10-08T13:34:24")).toBe("1:34 pm");
});

test("midnight and noon are twelve o'clock", () => {
    expect(formatTime("2026-10-08T00:05:00")).toBe("12:05 am");
    expect(formatTime("2026-10-08T12:00:00")).toBe("12:00 pm");
});

test("day has its weekday and month in short", () => {
    expect(formatDay("2026-10-09")).toBe("Fri, Oct 9");
    expect(formatDay("2027-01-01T05:00:00")).toBe("Fri, Jan 1");
});

test("duration is in hours and minutes", () => {
    expect(formatDuration(26014)).toBe("7 h 14 min");
    expect(formatDuration(3 * 3600)).toBe("3 h");
});

test("duration of less than an hour is in minutes", () => {
    expect(formatDuration(45 * 60)).toBe("45 min");
    expect(formatDuration(20)).toBe("0 min");
});

test("distance is in whole kilometres", () => {
    expect(formatDistance(144.42090000000002)).toBe("144 km");
});

test("seconds between two times are counted across midnight", () => {
    expect(secondsBetween("2026-10-08T23:30:00", "2026-10-09T00:44:00")).toBe(74 * 60);
});

test("days between two times count the midnights passed, however short the time", () => {
    expect(daysBetween("2026-10-08T06:00:00", "2026-10-08T23:59:00")).toBe(0);
    expect(daysBetween("2026-10-08T23:30:00", "2026-10-09T00:44:00")).toBe(1);
});

test("days are added across the end of a month", () => {
    expect(addDays("2026-10-31", 1)).toBe("2026-11-01");
    expect(addDays("2026-10-08", 0)).toBe("2026-10-08");
});
