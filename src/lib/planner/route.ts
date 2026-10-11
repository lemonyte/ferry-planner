import type { Query } from "#lib/query.ts";

import { carConnections } from "./data/car-connections.ts";
import { ferryConnections } from "./data/ferry-connections.ts";
import {
    cities,
    type Location,
    type LocationId,
    locations,
    type Terminal,
    type TerminalId,
    terminals,
} from "./data/locations.ts";
import type { Timetable } from "./gtfs.ts";
import type { Itinerary, Step } from "./itinerary.ts";
import { getSchedule } from "./schedule.ts";
import { formatLocal, MS_PER_DAY, MS_PER_MINUTE, startOfDay } from "./time.ts";

/** Maximum drive in seconds, unless `long` is set. */
const DRIVING_DURATION_LIMIT = 6 * 60 * 60;
const MAP_URL = "https://www.google.com/maps/dir/?api=1";

type Connection =
    | {
          type: "CAR";
          origin: Location;
          destination: Location;
          /** Duration in seconds. */
          duration: number;
          /** Distance in kilometers. */
          distance: number;
      }
    | { type: "FERRY"; origin: Terminal; destination: Terminal; bookable: boolean };

export interface PlanOptions {
    /** Local time on the day to travel on. */
    date: number;
    checkin: Query["checkin"];
    /** Minutes to arrive at a terminal before its check-in closes. */
    early: number;
    /** Whether to include long drives, overnight journeys, and sailings later than the first available. */
    long: boolean;
}

/** A step with local times in milliseconds, used until its itinerary is complete. */
type TimedStep = Omit<Step, "start" | "end"> & { start: number; end: number };

interface Segment {
    connection: Connection;
    steps: TimedStep[];
}

/**
 * Hash text to 11 base-36 characters.
 *
 * Not cryptographic. Used only to derive a short, stable ID.
 */
const hashText = (text: string): string => {
    let high = 0xdeadbeef;
    let low = 0x41c6ce57;
    for (let index = 0; index < text.length; index++) {
        const code = text.charCodeAt(index);
        high = Math.imul(high ^ code, 2654435761);
        low = Math.imul(low ^ code, 1597334677);
    }
    high = Math.imul(high ^ (high >>> 16), 2246822507) ^ Math.imul(low ^ (low >>> 13), 3266489909);
    low = Math.imul(low ^ (low >>> 16), 2246822507) ^ Math.imul(high ^ (high >>> 13), 3266489909);
    // 53 bits, the most that a number holds exactly.
    return ((low & 0x1fffff) * 2 ** 32 + (high >>> 0)).toString(36).padStart(11, "0");
};

const getConnection = (origin: LocationId, destination: LocationId): Connection | undefined => {
    const car = carConnections[origin]?.[destination];
    if (car) {
        return {
            type: "CAR",
            origin: locations[origin],
            destination: locations[destination],
            duration: car.duration,
            distance: car.distance,
        };
    }
    const ferry = ferryConnections[origin as TerminalId]?.[destination as TerminalId];
    return (
        ferry && {
            type: "FERRY",
            origin: terminals[origin as TerminalId],
            destination: terminals[destination as TerminalId],
            bookable: ferry.bookable,
        }
    );
};

/** Get the destination and type of each connection from a location, car connections first. */
const getConnectionsFrom = (origin: LocationId): [LocationId, Connection["type"]][] => {
    return [
        ...Object.keys(carConnections[origin] ?? {}).map((destination): [LocationId, Connection["type"]] => [
            destination as LocationId,
            "CAR",
        ]),
        ...Object.keys(ferryConnections[origin as TerminalId] ?? {}).map(
            (destination): [LocationId, Connection["type"]] => [destination as LocationId, "FERRY"],
        ),
    ];
};

/** Find the routes between two locations, each as a list of location IDs. */
export const findRoutes = (origin: LocationId, destination: LocationId): LocationId[][] => {
    const routes: LocationId[][] = [];
    const route: LocationId[] = [];
    const deadEnds = new Set<string>();
    // Land groups already left by ferry on this route. A route does not return to them.
    const lands: string[] = [];
    const endsInCity = destination in cities;

    const follow = (point: LocationId, lastType?: Connection["type"]): boolean => {
        route.push(point);
        if (point === destination) {
            routes.push([...route]);
            route.pop();
            return true;
        }
        if (endsInCity && getConnection(point, destination)) {
            routes.push([...route, destination]);
            route.pop();
            return true;
        }
        let found = false;
        for (const [next, type] of getConnectionsFrom(point)) {
            const id = `${point}-${next}`;
            if (route.includes(next) || deadEnds.has(id)) {
                continue;
            }
            // Drive only the shortest way between terminals.
            if (type === "CAR" && lastType === "CAR") {
                continue;
            }
            const landGroup = locations[next].land_group;
            if (type === "FERRY" && landGroup && lands.includes(landGroup)) {
                continue;
            }
            lands.push((type === "FERRY" && locations[point].land_group) || "");
            if (follow(next, type)) {
                found = true;
            } else {
                deadEnds.add(id);
            }
            lands.pop();
        }
        route.pop();
        return found;
    };

    follow(origin);
    return routes;
};

/** Find the ways to travel between two locations on a day. */
export const makeItineraries = (
    origin: LocationId,
    destination: LocationId,
    options: PlanOptions,
    timetable: Timetable,
    /** Current local time. */
    now: number,
): Itinerary[] => {
    const itineraries: Itinerary[] = [];
    for (const route of findRoutes(origin, destination)) {
        addItineraries({
            itineraries,
            route,
            index: 1,
            segments: [],
            startTime: startOfDay(options.date),
            options,
            timetable,
            now,
        });
    }
    return itineraries;
};

interface PlanState {
    itineraries: Itinerary[];
    route: LocationId[];
    /** Index in the route of the destination of the next segment. */
    index: number;
    /** Segments of the route so far. */
    segments: readonly Segment[];
    startTime: number;
    options: PlanOptions;
    timetable: Timetable;
    now: number;
}

/** Add itineraries for the rest of a route. Returns whether any were added. */
const addItineraries = (state: PlanState): boolean => {
    const { route, index, segments, startTime, options } = state;
    const [origin, destination] = [route[index - 1], route[index]];
    if (!origin || !destination) {
        // A route from a location to itself has no segments.
        if (segments.length > 0) {
            state.itineraries.push(makeItinerary(segments, state.now));
        }
        return segments.length > 0;
    }
    const connection = getConnection(origin, destination);
    if (connection?.type === "FERRY") {
        return addSailings(state, connection);
    }
    // Skip long drives.
    if (!connection || (!options.long && connection.duration > DRIVING_DURATION_LIMIT)) {
        return false;
    }
    const arriveTime = startTime + connection.duration * 1000;
    const drive: TimedStep = {
        // A zero-duration drive, between two places at the same location, is a point in time.
        kind: connection.duration > 0 ? "DRIVE" : "MARK",
        start: startTime,
        end: arriveTime,
        description: `Drive ${Math.round(connection.distance)} km to ${connection.destination.name}`,
    };
    return addItineraries({
        ...state,
        index: index + 1,
        segments: [...segments, { connection, steps: [drive] }],
        startTime: arriveTime,
    });
};

/** Get the name of the check-in deadline for a sailing, and its minutes before departure. */
const getDeadline = (
    origin: Terminal,
    bookable: boolean,
    checkin: Query["checkin"],
): [name: string, minutes: number] => {
    if (checkin === "hostled" && origin.hostled_close) {
        return ["hostled vehicles check-in close", origin.hostled_close];
    }
    if (checkin === "assured" && origin.assured_close) {
        return ["assured loading check-in close", origin.assured_close];
    }
    if (origin.res_close && bookable) {
        return ["booking check-in close", origin.res_close];
    }
    if (origin.veh_close) {
        return ["vehicles check-in close", origin.veh_close];
    }
    if (origin.foot_close) {
        return ["foot passengers check-in close", origin.foot_close];
    }
    return ["departure", 0];
};

/** Add itineraries for the rest of a route, for each sailing that can be caught. Returns whether any were added. */
const addSailings = (state: PlanState, connection: Connection & { type: "FERRY" }): boolean => {
    const { index, segments, startTime, options } = state;
    const { origin, destination } = connection;
    const day = startOfDay(startTime);
    // Skip routes that continue on another day.
    if (day !== startOfDay(segments[0]?.steps[0]?.start ?? startTime)) {
        return false;
    }
    const schedule = getSchedule(state.timetable, origin.id as TerminalId, destination.id as TerminalId, day);
    const [deadlineName, deadlineMinutes] = getDeadline(origin, connection.bookable, options.checkin);
    let found = false;
    for (const sailing of schedule.sailings) {
        // Skip routes that take more than one day.
        if (!options.long && sailing.arrival - startTime > MS_PER_DAY) {
            break;
        }
        const deadlineTime = sailing.departure - (deadlineMinutes + options.early) * MS_PER_MINUTE;
        if (deadlineTime < startTime) {
            continue;
        }
        const steps: TimedStep[] = [
            {
                kind: "FERRY",
                start: sailing.departure,
                end: sailing.arrival,
                description: `Ferry sailing from ${origin.name} to ${destination.name}`,
                scheduleUrl: schedule.url,
                from: origin.id as TerminalId,
                to: destination.id as TerminalId,
            },
        ];
        if (deadlineTime < sailing.departure) {
            const early = options.early > 0 ? `${options.early} minutes ` : "";
            steps.unshift({
                kind: "WAIT",
                start: deadlineTime,
                end: sailing.departure,
                description: `Arrive at ${origin.name} ${early}before ${deadlineName}`,
            });
        }
        const rest = { ...state, index: index + 1, segments: [...segments, { connection, steps }] };
        if (!addItineraries({ ...rest, startTime: sailing.arrival })) {
            break;
        }
        found = true;
        // After the first ferry of a route, take only the first sailing that can be caught.
        if (!options.long && segments.some((segment) => segment.connection.type === "FERRY")) {
            break;
        }
    }
    return found;
};

const mapParameter = (location: Location): string => {
    return "coordinates" in location
        ? location.coordinates
        : `${location.name},${location.province},${location.country}`;
};

const makeItinerary = (routeSegments: readonly Segment[], now: number): Itinerary => {
    const segments = routeSegments.map((segment) => ({
        ...segment,
        steps: segment.steps.map((step) => ({ ...step })),
    }));
    const first = segments[0];
    const last = segments.at(-1);
    if (!first || !last) {
        throw new Error("itinerary must have at least one segment");
    }
    if (first.connection.type === "CAR") {
        const next = segments[1];
        // Delay a leading drive to arrive just in time for the ferry.
        // A drive with no ferry starts at the current time of day.
        const shift = next
            ? (next.steps[0]?.start ?? 0) - (first.steps.at(-1)?.end ?? 0)
            : now - startOfDay(now) - (now % 1000);
        for (const step of first.steps) {
            step.start += shift;
            step.end += shift;
        }
    }
    for (const [index, segment] of segments.entries()) {
        const freeStart = segment.steps.at(-1)?.end;
        const freeEnd = segments[index + 1]?.steps[0]?.start;
        if (freeStart !== undefined && freeEnd !== undefined && freeEnd > freeStart) {
            segment.steps.push({ kind: "FREE", start: freeStart, end: freeEnd, description: "Free time" });
        }
    }
    const departTime = first.steps[0]?.start ?? 0;
    if (first.connection.type !== "FERRY") {
        first.steps.unshift({
            kind: "MARK",
            start: departTime,
            end: departTime,
            description: `Depart from ${first.connection.origin.name}`,
        });
    }
    const arriveTime = last.steps.at(-1)?.end ?? 0;
    last.steps.push({
        kind: "MARK",
        start: arriveTime,
        end: arriveTime,
        description: `Arrive at ${last.connection.destination.name}`,
    });

    let drivingDistance = 0;
    // The ID is derived from the route and its sailings only. It excludes the search time, at which a drive
    // with no ferry starts, so that the same itinerary keeps its ID in later searches.
    const parts: string[] = [];
    for (const { connection, steps } of segments) {
        if (connection.type === "CAR") {
            drivingDistance += connection.distance;
        }
        parts.push(connection.destination.id);
        for (const step of steps) {
            if (step.kind === "FERRY") {
                parts.push(formatLocal(step.start), formatLocal(step.end));
            }
        }
    }
    const waypoints = segments.slice(1).map((segment) => mapParameter(segment.connection.origin));
    return {
        id: hashText(parts.join(" ")),
        route: [first.connection.origin.id, ...segments.map((segment) => segment.connection.destination.id)].join("-"),
        depart: formatLocal(departTime),
        arrive: formatLocal(arriveTime),
        duration: (arriveTime - departTime) / 1000,
        drivingDistance,
        mapUrl:
            `${MAP_URL}&origin=${encodeURIComponent(mapParameter(first.connection.origin))}` +
            `&destination=${encodeURIComponent(mapParameter(last.connection.destination))}` +
            `&waypoints=${encodeURIComponent(waypoints.join("|"))}`,
        steps: segments.flatMap((segment) =>
            segment.steps.map((step) => ({ ...step, start: formatLocal(step.start), end: formatLocal(step.end) })),
        ),
    };
};
