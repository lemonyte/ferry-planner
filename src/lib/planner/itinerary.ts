// What a search gives, kept apart from the code that makes it so that pages can use the types on their own.

import type { LocationId } from "./data/locations";

export interface Step {
    /** `MARK` is a moment, such as the departure, and `FREE` is extra time between two other steps. */
    kind: "DRIVE" | "WAIT" | "FERRY" | "FREE" | "MARK";
    start: string;
    end: string;
    description: string;
    /** URL of the schedule that a sailing is from. */
    scheduleUrl?: string;
    /** Terminal that a sailing leaves from. */
    from?: LocationId;
    /** Terminal that a sailing arrives at. */
    to?: LocationId;
}

export interface Itinerary {
    /** Identifies the itinerary among those of a search, to find it again by. */
    id: string;
    /** Identifies the route, which is the locations gone through, among those of a search. */
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
    /** Itineraries worth taking, by departure. */
    itineraries: Itinerary[];
    /** Number of routes whose itineraries are not shown. */
    moreRoutes: number;
    /** Number of itineraries left out because they have already left, or arrived when those under way are shown. */
    departed: number;
    /** Number of those left out that have not arrived yet. */
    underway: number;
}

/** What routes are the best by, and so which are shown. */
export type Sort = "duration" | "departure" | "arrival";

/** Itineraries worth taking for a journey. */
export interface SearchResult extends Selection {
    origin: LocationId;
    destination: LocationId;
    /** Day of the journey, as `YYYY-MM-DD`. */
    date: string;
    /** Whether the feed has schedules for the day. */
    covered: boolean;
    /** Time of the search, which tells the itineraries that have already left. */
    now: string;
}
