// A search is stored in the URL query string, so that it can be linked to.

import { formatLocal, parseLocal, toLocal } from "./planner/time.ts";

export const CHECKINS = ["reservation", "assured", "hostled"] as const;
/** Default minutes to arrive at a terminal before its check-in closes. */
export const DEFAULT_EARLY = 15;
export const MAX_EARLY = 120;
/** Sort orders for trips. The first is the default. */
export const SORTS = ["duration", "departure", "arrival"] as const;

export interface Query {
    /** ID of the origin place, or an empty string if none is selected. */
    from: string;
    to: string;
    /** Day of the journey, as `YYYY-MM-DD`. */
    date: string;
    checkin: (typeof CHECKINS)[number];
    /** Minutes to arrive at a terminal before its check-in closes. */
    early: number;
    /** Whether to include long drives and overnight journeys. */
    long: boolean;
    /** Whether to show every trip instead of only the first few. */
    all: boolean;
    /** Sort order of the trips. */
    sort: (typeof SORTS)[number];
    /** Whether to group trips by route. */
    group: boolean;
    /** Whether to show trips that have departed but not arrived. */
    underway: boolean;
}

/** Parse a search from URL query parameters, using defaults for missing or invalid values. */
export const parseQuery = (params: URLSearchParams, today: string): Query => {
    const date = params.get("date") ?? "";
    const checkin = CHECKINS.find((checkin) => checkin === params.get("checkin"));
    const early = Number(params.get("early") ?? DEFAULT_EARLY);
    return {
        from: params.get("from") ?? "",
        to: params.get("to") ?? "",
        // Reject dates that do not exist, such as June 31.
        date: /^\d{4}-\d{2}-\d{2}$/.test(date) && parseLocal(date) !== undefined ? date : today,
        checkin: checkin ?? "reservation",
        early: Number.isInteger(early) && early >= 0 && early <= MAX_EARLY ? early : DEFAULT_EARLY,
        long: params.get("long") === "1",
        all: params.get("all") === "1",
        sort: SORTS.find((sort) => sort === params.get("sort")) ?? "duration",
        group: params.get("group") === "route",
        underway: params.get("underway") === "1",
    };
};

/** Read the search from a URL. The date defaults to the current day in British Columbia. */
export const readQuery = (url: URL): Query => {
    return parseQuery(url.searchParams, formatLocal(toLocal(Date.now())).slice(0, 10));
};

/** Serialize a search as a URL query string, omitting defaults. */
export const toSearch = (query: Query): string => {
    const params = new URLSearchParams({
        from: query.from,
        to: query.to,
        date: query.date,
        ...(query.checkin !== "reservation" && { checkin: query.checkin }),
        ...(query.early !== DEFAULT_EARLY && { early: String(query.early) }),
        ...(query.long && { long: "1" }),
        ...(query.all && { all: "1" }),
        ...(query.sort !== "duration" && { sort: query.sort }),
        ...(query.group && { group: "route" }),
        ...(query.underway && { underway: "1" }),
    });
    return `?${params}`;
};
