import type { Query } from "./query.ts";
import type { Itinerary } from "./types.ts";

const COMPARE: Record<Query["sort"], (a: Itinerary, b: Itinerary) => number> = {
    duration: (a, b) => a.duration - b.duration || a.depart.localeCompare(b.depart),
    departure: (a, b) => a.depart.localeCompare(b.depart) || a.arrive.localeCompare(b.arrive),
    // Of the trips that arrive together, the one that leaves last comes first.
    arrival: (a, b) => a.arrive.localeCompare(b.arrive) || b.depart.localeCompare(a.depart),
};

/** Put trips in order of how long they take, or of when they leave or arrive. */
export const sortItineraries = (itineraries: Itinerary[], sort: Query["sort"]): Itinerary[] => {
    return itineraries.toSorted(COMPARE[sort]);
};
