import { building } from "$app/env";

import type { SearchResult } from "#lib/planner/itinerary.ts";
import { parseQuery, type Query, readQuery } from "#lib/query.ts";
import { getPlanner, hasSchedules, SCHEDULES } from "#lib/schedules.svelte.ts";

// Prerendered as the home page without a search. The same HTML is served for a search, which the browser then renders.
export const prerender = true;
export const ssr = true;

/** Result of a search: the trips found, or an error message. */
interface Outcome {
    result?: SearchResult;
    error?: string;
}

interface Data {
    query: Query;
    /** A promise if the search has to wait for the schedules to download. */
    outcome: Outcome | Promise<Outcome>;
}

const search = async (query: Query): Promise<Outcome> => {
    try {
        const planner = await getPlanner();
        if (!planner) {
            return { error: "Schedules have not been downloaded yet. Connect to the internet to get them." };
        }
        const result = planner.search(query);
        return result ? { result } : { error: "Choose both places from the list." };
    } catch (error) {
        console.error("failed to search", error);
        return { error: "Trips could not be looked up right now. Please try again in a minute." };
    }
};

export const load = async ({ url, depends }): Promise<Data> => {
    depends(SCHEDULES);
    // A prerendered page has no query string or current day.
    const query = building ? parseQuery(new URLSearchParams(), "") : readQuery(url);
    if (!query.from || !query.to) {
        return { query, outcome: {} };
    }
    if (query.from === query.to) {
        return { query, outcome: { error: "Choose two different places." } };
    }
    // If the schedules still have to download, stream the result so that the page renders without waiting.
    return { query, outcome: hasSchedules() ? await search(query) : search(query) };
};
