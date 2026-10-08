import { type Query, toBackendQuery } from "#lib/query.ts";
import { fetchBackend } from "#lib/server/backend.ts";
import { readQuery } from "#lib/server/query.ts";
import type { SearchResult } from "#lib/types.ts";

const UNAVAILABLE = "Schedules are not available right now. Please try again in a minute.";

/** What came of a search: the trips found, or what to say in place of them. */
interface Outcome {
    result?: SearchResult;
    error?: string;
}

interface Data {
    query: Query;
    /** Still to come when the page is sent, for a search that is too much for the server to lay out itself. */
    outcome: Outcome | Promise<Outcome>;
}

const search = async (query: Query): Promise<Outcome> => {
    try {
        const response = await fetchBackend(`/api/search?${toBackendQuery(query)}`);
        if (response.ok) {
            return { result: await response.json<SearchResult>() };
        }
        // The backend only refuses a search for places that it does not know, as the rest is checked here.
        return { error: response.status === 422 ? "Choose both places from the list." : UNAVAILABLE };
    } catch (error) {
        console.error(JSON.stringify({ message: "failed to reach the backend", error: String(error) }));
        return { error: UNAVAILABLE };
    }
};

export const load = async ({ url }): Promise<Data> => {
    const query = readQuery(url);
    if (!query.from || !query.to) {
        return { query, outcome: {} };
    }
    if (query.from === query.to) {
        return { query, outcome: { error: "Choose two different places." } };
    }
    // Laying out every route takes the server more CPU time than a Worker gets on the Workers Free plan,
    // so those are sent on after the page for the browser to lay out.
    return { query, outcome: query.all ? search(query) : await search(query) };
};
