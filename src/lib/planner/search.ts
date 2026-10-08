import type { Itinerary, Selection, Sort, Step } from "./api";
import type { LocationId } from "./data/locations";
import type { RoutePlan } from "./route";

/** Number of routes shown unless all are asked for. */
const BEST_ROUTES = 3;

export interface SelectOptions {
    /** Whether to show every route there is. */
    all?: boolean;
    /** What the routes shown are the best by. */
    sort?: Sort;
    /** Whether to show the itineraries that have left but not arrived yet. */
    underway?: boolean;
}

const COMPARE: Record<Sort, (a: RoutePlan, b: RoutePlan) => number> = {
    duration: (a, b) => a.duration - b.duration,
    departure: (a, b) => a.depart_time.localeCompare(b.depart_time),
    arrival: (a, b) => a.arrive_time.localeCompare(b.arrive_time),
};

interface Candidate {
    plan: RoutePlan;
    route: string;
    ferries: number;
}

/** Check if an itinerary leaves no earlier, arrives no later, and uses no more ferries than another. */
const isAsGood = (a: Candidate, b: Candidate): boolean => {
    return (
        a.plan.depart_time >= b.plan.depart_time && a.plan.arrive_time <= b.plan.arrive_time && a.ferries <= b.ferries
    );
};

/** Get the itineraries that no other one is better than, keeping the one with the least driving of those alike. */
const worthTaking = (candidates: Candidate[]): Candidate[] => {
    return candidates.filter(
        (candidate, index) =>
            !candidates.some(
                (other, otherIndex) =>
                    otherIndex !== index &&
                    isAsGood(other, candidate) &&
                    // One of two that are as good as each other still has to be kept.
                    (!isAsGood(candidate, other) ||
                        other.plan.driving_distance < candidate.plan.driving_distance ||
                        (other.plan.driving_distance === candidate.plan.driving_distance && otherIndex < index)),
            ),
    );
};

const toId = (plan: RoutePlan): string => {
    return plan.hash.slice(0, 12);
};

const toRoute = (plan: RoutePlan): string => {
    return [plan.segments[0]?.connection.origin.id, ...plan.segments.map((s) => s.connection.destination.id)].join(
        "-",
    );
};

const toItinerary = (plan: RoutePlan): Itinerary => {
    return {
        id: toId(plan),
        route: toRoute(plan),
        depart: plan.depart_time,
        arrive: plan.arrive_time,
        duration: plan.duration,
        drivingDistance: plan.driving_distance,
        mapUrl: plan.map_url,
        steps: plan.segments.flatMap((segment) =>
            segment.times.map((time): Step => {
                if (time.type !== "TRAVEL") {
                    return { kind: time.type, start: time.start, end: time.end, description: time.description };
                }
                if (time.start === time.end) {
                    return { kind: "MARK", start: time.start, end: time.end, description: time.description };
                }
                return segment.connection.type === "FERRY"
                    ? {
                          kind: "FERRY",
                          start: time.start,
                          end: time.end,
                          description: time.description,
                          scheduleUrl: segment.schedule_url,
                          from: segment.connection.origin.id as LocationId,
                          to: segment.connection.destination.id as LocationId,
                      }
                    : { kind: "DRIVE", start: time.start, end: time.end, description: time.description };
            }),
        ),
    };
};

/** Group itineraries into their routes, the route with the best itinerary first. */
const toRoutes = (candidates: Candidate[], compare: (a: RoutePlan, b: RoutePlan) => number): Candidate[][] => {
    return [...Map.groupBy(candidates, (candidate) => candidate.route).values()]
        .map((route) => route.toSorted((a, b) => compare(a.plan, b.plan)))
        .sort(([a], [b]) => (a && b ? compare(a.plan, b.plan) : 0));
};

/**
 * Pick the itineraries worth taking from all the ways there are to make a journey.
 *
 * An itinerary is worth taking unless another leaves no earlier, arrives no later, and uses no more ferries.
 * Only those of the routes with the best itineraries are shown: the fastest, or the first to leave or arrive.
 * With `all`, so are those of the other routes, and of the routes that are never worth taking, each with
 * the itineraries worth taking of its own.
 */
export const selectItineraries = (plans: RoutePlan[], now: string, options: SelectOptions = {}): Selection => {
    const { all = false, sort = "duration", underway = false } = options;
    const left = plans.filter((plan) => plan.depart_time < now);
    const leftOut = underway ? left.filter((plan) => plan.arrive_time < now) : left;
    const candidates = plans
        .filter((plan) => !leftOut.includes(plan))
        .map((plan) => ({
            plan,
            route: toRoute(plan),
            ferries: plan.segments.filter((segment) => segment.connection.type === "FERRY").length,
        }));
    const best = worthTaking(candidates);
    const routes = toRoutes(best, COMPARE[sort]);
    const bestRoutes = new Set(best.map((candidate) => candidate.route));
    const others = toRoutes(
        candidates.filter((candidate) => !bestRoutes.has(candidate.route)),
        COMPARE[sort],
    ).map(worthTaking);
    const shown = all ? [...routes, ...others] : routes.slice(0, BEST_ROUTES);
    return {
        itineraries: shown
            .flat()
            .map((candidate) => candidate.plan)
            .sort((a, b) => a.depart_time.localeCompare(b.depart_time) || a.arrive_time.localeCompare(b.arrive_time))
            .map(toItinerary),
        moreRoutes: routes.length + others.length - shown.length,
        departed: leftOut.length,
        underway: leftOut.filter((plan) => plan.arrive_time >= now).length,
    };
};

/** Find the itinerary with an ID among all the ways there are to make a journey. */
export const findItinerary = (plans: RoutePlan[], id: string): Itinerary | undefined => {
    const plan = plans.find((plan) => toId(plan) === id);
    return plan && toItinerary(plan);
};
