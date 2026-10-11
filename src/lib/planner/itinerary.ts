import type { LocationId } from "./data/locations.ts";

export interface Step {
    /** `MARK` is a point in time, such as the departure. `FREE` is spare time between two other steps. */
    kind: "DRIVE" | "WAIT" | "FERRY" | "FREE" | "MARK";
    start: string;
    end: string;
    description: string;
    /** BC Ferries schedule URL of a sailing. */
    scheduleUrl?: string;
    /** Departure terminal of a sailing. */
    from?: LocationId;
    /** Arrival terminal of a sailing. */
    to?: LocationId;
}

export interface Itinerary {
    /** Unique among the itineraries of a search. */
    id: string;
    /** IDs of the locations on the route, joined by `-`. */
    route: string;
    depart: string;
    arrive: string;
    /** Total duration in seconds. */
    duration: number;
    /** Total driving distance in kilometers. */
    drivingDistance: number;
    /** Google Maps URL of the route. */
    mapUrl: string;
    steps: Step[];
}

export interface Selection {
    /** Itineraries shown, in the requested sort order. */
    itineraries: Itinerary[];
    /** Number of itineraries not shown. */
    more: number;
    /** Number of itineraries excluded because they have departed, or arrived if `underway` is set. */
    departed: number;
    /** Number of excluded itineraries that have not arrived yet. */
    underway: number;
}

export interface SearchResult extends Selection {
    /** Whether the feed covers the day. */
    covered: boolean;
    /** Local time of the search, used to tell which itineraries have departed. */
    now: string;
}
