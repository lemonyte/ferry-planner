import type { Query } from "#lib/query.ts";
import { compareItineraries } from "#lib/sort.ts";

import type { Itinerary, Selection } from "./itinerary.ts";

/** Number of itineraries shown unless `all` is set. */
const SHOWN = 10;

export type SelectOptions = Pick<Query, "all" | "sort" | "underway">;

/** Check if an itinerary leaves no earlier and arrives no later than another. */
const isAsGood = (a: Itinerary, b: Itinerary): boolean => {
    return a.depart >= b.depart && a.arrive <= b.arrive;
};

/**
 * Check if an itinerary is redundant because another on the same route is as good or better.
 *
 * Itineraries on a route use the same ferries and drives, so one that departs earlier without arriving
 * sooner is the same journey with a longer wait.
 */
const isNoUse = (itinerary: Itinerary, index: number, itineraries: Itinerary[]): boolean => {
    return itineraries.some(
        (other, otherIndex) =>
            otherIndex !== index &&
            other.route === itinerary.route &&
            isAsGood(other, itinerary) &&
            // Of two equally good itineraries, keep the first.
            (!isAsGood(itinerary, other) || otherIndex < index),
    );
};

/**
 * Select the itineraries to show from every itinerary of a journey.
 *
 * Sorts by `options.sort` and returns the first `SHOWN`, or all of them if `options.all` is set.
 */
export const selectItineraries = (itineraries: Itinerary[], now: string, options: SelectOptions): Selection => {
    const isLeftOut = (itinerary: Itinerary): boolean => (options.underway ? itinerary.arrive : itinerary.depart) < now;
    const leftOut = itineraries.filter(isLeftOut);
    const ranked = itineraries
        .filter((itinerary) => !isLeftOut(itinerary))
        .filter((itinerary, index, candidates) => !isNoUse(itinerary, index, candidates))
        .sort(compareItineraries[options.sort]);
    const shown = options.all ? ranked : ranked.slice(0, SHOWN);
    return {
        itineraries: shown,
        more: ranked.length - shown.length,
        departed: leftOut.length,
        underway: leftOut.filter((itinerary) => itinerary.arrive >= now).length,
    };
};
