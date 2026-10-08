// A search is kept in the query of the URL, so that it can be linked to.

export const CHECKINS = ["reservation", "assured", "hostled"] as const;
/** Minutes to arrive at a terminal before its check-in closes, unless asked otherwise. */
export const DEFAULT_EARLY = 15;
export const MAX_EARLY = 120;
/** What trips can be put in order of, the first unless asked otherwise. */
export const SORTS = ["duration", "departure", "arrival"] as const;

export interface Query {
    /** ID of the place to leave from, or nothing when none has been picked. */
    from: string;
    to: string;
    /** Day of the journey, as `YYYY-MM-DD`. */
    date: string;
    checkin: (typeof CHECKINS)[number];
    /** Minutes to arrive at a terminal before its check-in closes. */
    early: number;
    /** Whether to include long drives and journeys that go on overnight. */
    long: boolean;
    /** Whether to show every route there is. */
    all: boolean;
    /** What the trips are in order of. */
    sort: (typeof SORTS)[number];
    /** Whether the trips of a route are shown together. */
    group: boolean;
    /** Whether to show the trips that have left but not arrived yet. */
    underway: boolean;
}

/** Read a search from the query of a URL, with the usual in place of anything missing or wrong. */
export const parseQuery = (params: URLSearchParams, today: string): Query => {
    const date = params.get("date") ?? "";
    const checkin = CHECKINS.find((checkin) => checkin === params.get("checkin"));
    const early = Number(params.get("early") ?? DEFAULT_EARLY);
    return {
        from: params.get("from") ?? "",
        to: params.get("to") ?? "",
        date: /^\d{4}-\d{2}-\d{2}$/.test(date) && !Number.isNaN(Date.parse(date)) ? date : today,
        checkin: checkin ?? "reservation",
        early: Number.isInteger(early) && early >= 0 && early <= MAX_EARLY ? early : DEFAULT_EARLY,
        long: params.get("long") === "1",
        all: params.get("routes") === "all",
        sort: SORTS.find((sort) => sort === params.get("sort")) ?? "duration",
        group: params.get("group") === "route",
        underway: params.get("underway") === "1",
    };
};

/** Write a search as the query that the backend takes. */
export const toBackendQuery = (query: Query): string => {
    const params = new URLSearchParams({
        origin: query.from,
        destination: query.to,
        date: query.date,
        buffer: String(query.early),
    });
    if (query.checkin === "assured") {
        params.set("assured", "true");
    }
    if (query.checkin === "hostled") {
        params.set("hostled", "true");
    }
    if (query.long) {
        params.set("show_all", "true");
    }
    if (query.all) {
        params.set("routes", "all");
    }
    // The routes shown are the best by what the trips are in order of.
    if (query.sort !== "duration") {
        params.set("sort", query.sort);
    }
    if (query.underway) {
        params.set("underway", "true");
    }
    return params.toString();
};

/** Write a search as the query of a link to it, leaving out what is as usual. */
export const toSearch = (query: Query): string => {
    const params = new URLSearchParams({ from: query.from, to: query.to, date: query.date });
    if (query.checkin !== "reservation") {
        params.set("checkin", query.checkin);
    }
    if (query.early !== DEFAULT_EARLY) {
        params.set("early", String(query.early));
    }
    if (query.long) {
        params.set("long", "1");
    }
    if (query.all) {
        params.set("routes", "all");
    }
    if (query.sort !== "duration") {
        params.set("sort", query.sort);
    }
    if (query.group) {
        params.set("group", "route");
    }
    if (query.underway) {
        params.set("underway", "1");
    }
    return `?${params}`;
};
