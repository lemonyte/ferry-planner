import type { Itinerary } from "./planner/itinerary.ts";
import type { Query } from "./query.ts";

/** Comparator for each sort order. */
export const compareItineraries: Record<Query["sort"], (a: Itinerary, b: Itinerary) => number> = {
    duration: (a, b) => a.duration - b.duration || a.depart.localeCompare(b.depart),
    departure: (a, b) => a.depart.localeCompare(b.depart) || a.arrive.localeCompare(b.arrive),
    // Of trips that arrive together, the latest departure comes first.
    arrival: (a, b) => a.arrive.localeCompare(b.arrive) || b.depart.localeCompare(a.depart),
};
