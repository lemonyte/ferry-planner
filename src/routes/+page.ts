import { type Query, readQuery } from "#lib/query.ts";
import { getPlanner, hasSchedules, SCHEDULES } from "#lib/schedules.svelte.ts";
import type { SearchResult } from "#lib/types.ts";

/** What came of a search: the trips found, or what to say in place of them. */
interface Outcome {
    result?: SearchResult;
    error?: string;
}

interface Data {
    query: Query;
    /** Still to come when the page is shown, for a search that has to wait for the schedules to be downloaded. */
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
    const query = readQuery(url);
    if (!query.from || !query.to) {
        return { query, outcome: {} };
    }
    if (query.from === query.to) {
        return { query, outcome: { error: "Choose two different places." } };
    }
    // The first search of a first visit is shown once the schedules are there, and the page without waiting for it.
    return { query, outcome: hasSchedules() ? await search(query) : search(query) };
};
