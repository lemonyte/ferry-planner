import { error } from "@sveltejs/kit";

import type { Itinerary } from "#lib/planner/itinerary.ts";
import { type Query, readQuery } from "#lib/query.ts";
import { getPlanner, SCHEDULES } from "#lib/schedules.svelte.ts";

interface Data {
    /** Search that the trip belongs to. */
    query: Query;
    itinerary: Itinerary;
}

export const load = async ({ params, url, depends }): Promise<Data> => {
    depends(SCHEDULES);
    const query = readQuery(url);
    const planner = await getPlanner().catch((error: unknown) => {
        console.error("failed to load the planner", error);
    });
    if (!planner) {
        error(503, "Schedules have not been downloaded yet. Connect to the internet to get them.");
    }
    const itinerary = planner.itinerary(query, params.id);
    // A trip is missing only if its link is wrong or the schedules have changed.
    if (!itinerary) {
        error(404, "This trip is no longer available. The schedules may have changed since the link to it was made.");
    }
    return { query, itinerary };
};
