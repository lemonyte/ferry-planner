import { error } from "@sveltejs/kit";
import { type Query, toBackendQuery } from "#lib/query.ts";
import { fetchBackend } from "#lib/server/backend.ts";
import { readQuery } from "#lib/server/query.ts";
import type { Itinerary } from "#lib/types.ts";

interface Data {
    /** Search that the trip is from. */
    query: Query;
    itinerary: Itinerary;
}

export const load = async ({ params, url }): Promise<Data> => {
    const query = readQuery(url);
    const response = await fetchBackend(
        `/api/itinerary?${toBackendQuery(query)}&id=${encodeURIComponent(params.id)}`,
    ).catch((error: unknown) => {
        console.error(JSON.stringify({ message: "failed to reach the backend", error: String(error) }));
    });
    if (response?.ok) {
        return { query, itinerary: await response.json<Itinerary>() };
    }
    // A trip is only not found, or its search refused, when the link to it is wrong or the schedules have changed.
    if (response?.status === 404 || response?.status === 422) {
        error(404, "This trip is no longer available. The schedules may have changed since the link to it was made.");
    }
    error(503, "Schedules are not available right now. Please try again in a minute.");
};
