import type { Itinerary } from "#lib/planner/itinerary.ts";

/** Summarize an itinerary as its times, its route, and the departure times of its sailings. */
export const summarize = (itinerary: Itinerary): string => {
    const sailings = itinerary.steps.filter((step) => step.kind === "FERRY").map((step) => step.start.slice(11, 16));
    return `${itinerary.depart} > ${itinerary.arrive} ${itinerary.route} [${sailings.join(" ")}]`;
};
