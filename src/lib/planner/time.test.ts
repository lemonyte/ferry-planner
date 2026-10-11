import { expect, test } from "vitest";

import { formatLocal, parseLocal, startOfDay, toLocal } from "./time.ts";

test("parseLocal parses a date as the start of the day", () => {
    expect(parseLocal("2026-10-08")).toBe(Date.UTC(2026, 9, 8));
});

test("parseLocal ignores the UTC offset of a date and time", () => {
    expect(parseLocal("2026-10-08T05:30")).toBe(Date.UTC(2026, 9, 8, 5, 30));
    expect(parseLocal("2026-10-08T05:30:15+02:00")).toBe(Date.UTC(2026, 9, 8, 5, 30, 15));
    expect(parseLocal("2026-10-08T23:30:00Z")).toBe(Date.UTC(2026, 9, 8, 23, 30));
});

test("parseLocal returns undefined for an invalid date", () => {
    expect(parseLocal("tomorrow")).toBeUndefined();
    expect(parseLocal("2026-06-31")).toBeUndefined();
});

test("formatLocal omits the UTC offset", () => {
    expect(formatLocal(Date.UTC(2026, 9, 8, 5, 30))).toBe("2026-10-08T05:30:00");
});

test("startOfDay returns midnight", () => {
    expect(startOfDay(Date.UTC(2026, 9, 8, 23, 59, 59))).toBe(Date.UTC(2026, 9, 8));
    expect(startOfDay(Date.UTC(2026, 9, 8))).toBe(Date.UTC(2026, 9, 8));
});

// British Columbia stopped changing its clocks in 2026, so the years before are used here.
test("toLocal converts epoch milliseconds to Vancouver time", () => {
    expect(toLocal(Date.UTC(2025, 6, 8, 3))).toBe(Date.UTC(2025, 6, 7, 20));
    expect(toLocal(Date.UTC(2025, 11, 8, 3))).toBe(Date.UTC(2025, 11, 7, 19));
});
