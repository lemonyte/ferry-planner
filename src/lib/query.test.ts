import { expect, test } from "vitest";
import { parseQuery, type Query, toBackendQuery, toSearch } from "./query";

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

const parse = (search: string): Query => parseQuery(new URLSearchParams(search), TODAY);

test("search with only places is for today with the usual options", () => {
    expect(parse("from=vancouver&to=van_anda")).toEqual({ ...VAN_ANDA, date: TODAY });
});

test("search without places has none", () => {
    expect(parse("")).toMatchObject({ from: "", to: "", date: TODAY });
});

test("search reads every option", () => {
    expect(
        parse(
            "from=vancouver&to=van_anda&date=2026-10-09&checkin=assured&early=30&long=1&routes=all&sort=arrival&group=route&underway=1",
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
    ["a date that is not one", "date=soon", { date: TODAY }],
    ["a kind of check-in that there is not", "checkin=vip", { checkin: "reservation" }],
    ["an early arrival that is not a number", "early=very", { early: 15 }],
    ["an early arrival of less than nothing", "early=-5", { early: 15 }],
    ["an order that there is not", "sort=price", { sort: "duration" }],
])("search with %s falls back to the usual", (_, search, expected) => {
    expect(parse(search)).toMatchObject(expected);
});

test("backend is asked with its own names for the options", () => {
    expect(toBackendQuery(VAN_ANDA)).toBe("origin=vancouver&destination=van_anda&date=2026-10-09&buffer=15");
    expect(toBackendQuery({ ...VAN_ANDA, checkin: "assured", early: 30, long: true, all: true })).toBe(
        "origin=vancouver&destination=van_anda&date=2026-10-09&buffer=30&assured=true&show_all=true&routes=all",
    );
    expect(toBackendQuery({ ...VAN_ANDA, checkin: "hostled" })).toContain("hostled=true");
    expect(toBackendQuery({ ...VAN_ANDA, sort: "arrival", underway: true })).toBe(
        "origin=vancouver&destination=van_anda&date=2026-10-09&buffer=15&sort=arrival&underway=true",
    );
    // Trips are put together by route here, which the backend has no part in.
    expect(toBackendQuery({ ...VAN_ANDA, group: true })).toBe(toBackendQuery(VAN_ANDA));
});

test("link to a search leaves out the options that are as usual", () => {
    expect(toSearch(VAN_ANDA)).toBe("?from=vancouver&to=van_anda&date=2026-10-09");
    expect(toSearch({ ...VAN_ANDA, checkin: "hostled", early: 0, long: true, all: true, sort: "departure" })).toBe(
        "?from=vancouver&to=van_anda&date=2026-10-09&checkin=hostled&early=0&long=1&routes=all&sort=departure",
    );
});

test("link to a search is read back as the same search", () => {
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
