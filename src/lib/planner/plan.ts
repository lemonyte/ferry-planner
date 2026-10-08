// Searches as the pages ask for them. This is all that the pages need of the planner,
// so that the rest of it, and the connections that it goes by, are only loaded with this.

import type { Query } from "#lib/query.ts";
import { type LocationId, locations } from "./data/locations";
import type { Timetable } from "./gtfs";
import type { Itinerary, SearchResult } from "./itinerary";
import { type RoutePlan, routePlans } from "./route";
import { findItinerary, selectItineraries } from "./search";
import { formatLocal, parseLocal, startOfDay } from "./time";

interface Journey {
    origin: LocationId;
    destination: LocationId;
    /** Local time at the start of the day of the journey. */
    date: number;
    plans: RoutePlan[];
}

const isLocation = (id: string): id is LocationId => {
    return Object.hasOwn(locations, id);
};

/** Find all the ways there are to make the journey of a search, or nothing if it is not between two places. */
const findJourney = (query: Query, timetable: Timetable, now: number): Journey | undefined => {
    const date = parseLocal(query.date);
    if (!isLocation(query.from) || !isLocation(query.to) || query.from === query.to || date === undefined) {
        return undefined;
    }
    const plans = routePlans(
        query.from,
        query.to,
        {
            date,
            showAll: query.long,
            assured: query.checkin === "assured",
            hostled: query.checkin === "hostled",
            buffer: query.early,
        },
        timetable,
        now,
    );
    return { origin: query.from, destination: query.to, date, plans };
};

/**
 * Find the itineraries worth taking for a search, or nothing if it is not between two places that are known.
 *
 * `now` is the current local time, which tells the itineraries that have already left.
 */
export const search = (query: Query, timetable: Timetable, now: number): SearchResult | undefined => {
    const journey = findJourney(query, timetable, now);
    return (
        journey && {
            origin: journey.origin,
            destination: journey.destination,
            date: formatLocal(journey.date).slice(0, 10),
            covered: timetable.covers(startOfDay(journey.date)),
            now: formatLocal(now),
            ...selectItineraries(journey.plans, formatLocal(now), {
                all: query.all,
                sort: query.sort,
                underway: query.underway,
            }),
        }
    );
};

/** Find the itinerary of a search with an ID, whether the search shows it or not. */
export const itinerary = (query: Query, id: string, timetable: Timetable, now: number): Itinerary | undefined => {
    const journey = findJourney(query, timetable, now);
    return journey && findItinerary(journey.plans, id);
};
