import type { Query } from "#lib/query.ts";

import { type LocationId, locations } from "./data/locations.ts";
import type { Timetable } from "./gtfs.ts";
import type { Itinerary, SearchResult } from "./itinerary.ts";
import { makeItineraries } from "./route.ts";
import { selectItineraries } from "./search.ts";
import { formatLocal, parseLocal } from "./time.ts";

const isLocation = (id: string): id is LocationId => {
    return Object.hasOwn(locations, id);
};

/** Find every itinerary for a search, or `undefined` if its places or date are not valid. */
const findItineraries = (query: Query, timetable: Timetable, now: number): Itinerary[] | undefined => {
    const date = parseLocal(query.date);
    if (!isLocation(query.from) || !isLocation(query.to) || query.from === query.to || date === undefined) {
        return undefined;
    }
    const options = { date, checkin: query.checkin, early: query.early, long: query.long };
    return makeItineraries(query.from, query.to, options, timetable, now);
};

/**
 * Find the itineraries to show for a search, or `undefined` if its places or date are not valid.
 *
 * `now` is the current local time, used to tell which itineraries have departed.
 */
export const search = (query: Query, timetable: Timetable, now: number): SearchResult | undefined => {
    const itineraries = findItineraries(query, timetable, now);
    return (
        itineraries && {
            covered: timetable.covers(parseLocal(query.date) ?? Number.NaN),
            now: formatLocal(now),
            ...selectItineraries(itineraries, formatLocal(now), query),
        }
    );
};

/** Find an itinerary of a search by ID, whether or not the search shows it. */
export const itinerary = (query: Query, id: string, timetable: Timetable, now: number): Itinerary | undefined => {
    return findItineraries(query, timetable, now)?.find((itinerary) => itinerary.id === id);
};
