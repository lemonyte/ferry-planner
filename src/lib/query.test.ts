import { afterEach, expect, test, vi } from "vitest";

import { parseQuery, type Query, readQuery, toSearch } from "./query.ts";

const TODAY = "2026-10-08";
const VAN_ANDA: Query = {
    from: "vancouver",
    to: "van_anda",
    date: "2026-10-09",
    checkin: "reservation",
    early: 15,
    long: false,
    all: false,
    sort: "duration",
    group: false,
    underway: false,
};

afterEach(() => {
    vi.restoreAllMocks();
});

const parse = (search: string): Query => parseQuery(new URLSearchParams(search), TODAY);

test("parseQuery uses the current date and default options if only places are given", () => {
    expect(parse("from=vancouver&to=van_anda")).toEqual({ ...VAN_ANDA, date: TODAY });
});

test("parseQuery returns empty place IDs if no places are given", () => {
    expect(parse("")).toMatchObject({ from: "", to: "", date: TODAY });
});

test("parseQuery reads every option", () => {
    expect(
        parse(
            "from=vancouver&to=van_anda&date=2026-10-09&checkin=assured&early=30&long=1&all=1&sort=arrival&group=route&underway=1",
        ),
    ).toEqual({
        ...VAN_ANDA,
        group: true,
        underway: true,
        checkin: "assured",
        early: 30,
        long: true,
        all: true,
        sort: "arrival",
    });
});

test.each([
    ["an invalid date", "date=soon", { date: TODAY }],
    ["a date that does not exist", "date=2026-02-31", { date: TODAY }],
    ["a date with a time", "date=2026-10-09T10:00", { date: TODAY }],
    ["an unknown check-in type", "checkin=vip", { checkin: "reservation" }],
    ["a non-numeric early arrival", "early=very", { early: 15 }],
    ["a negative early arrival", "early=-5", { early: 15 }],
    ["an unknown sort order", "sort=price", { sort: "duration" }],
])("parseQuery uses the default for %s", (_, search, expected) => {
    expect(parse(search)).toMatchObject(expected);
});

test("readQuery defaults the date to the current day in British Columbia", () => {
    // Late in the evening of the 8th in British Columbia.
    vi.spyOn(Date, "now").mockReturnValue(Date.UTC(2026, 9, 9, 5));

    expect(readQuery(new URL("https://site/?from=vancouver&to=van_anda")).date).toBe("2026-10-08");
    expect(readQuery(new URL("https://site/?from=vancouver&to=van_anda&date=2026-10-12")).date).toBe("2026-10-12");
});

test("toSearch omits options that are set to their defaults", () => {
    expect(toSearch(VAN_ANDA)).toBe("?from=vancouver&to=van_anda&date=2026-10-09");
    expect(toSearch({ ...VAN_ANDA, checkin: "hostled", early: 0, long: true, all: true, sort: "departure" })).toBe(
        "?from=vancouver&to=van_anda&date=2026-10-09&checkin=hostled&early=0&long=1&all=1&sort=departure",
    );
});

test("toSearch output parses back to the same search", () => {
    const query: Query = {
        ...VAN_ANDA,
        checkin: "assured",
        early: 45,
        long: true,
        all: true,
        sort: "arrival",
        group: true,
        underway: true,
    };

    expect(parse(toSearch(query).slice(1))).toEqual(query);
});
