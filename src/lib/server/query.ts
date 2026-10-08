import { parseQuery, type Query } from "#lib/query.ts";

const DAY_FORMAT = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Vancouver" });

/** Read the search in a URL, for the current day in British Columbia unless it says another. */
export const readQuery = (url: URL): Query => {
    return parseQuery(url.searchParams, DAY_FORMAT.format(new Date()));
};
