import { createHash } from "node:crypto";
import { carConnections } from "./data/car-connections";
import { ferryConnections } from "./data/ferry-connections";
import { cities, type Location, type LocationId, locations, type Terminal, type TerminalId } from "./data/locations";
import type { Timetable } from "./gtfs";
import { getSchedule } from "./schedule";
import { formatLocal, MS_PER_DAY, MS_PER_MINUTE, startOfDay } from "./time";

/** Longest drive in seconds that is shown unless all route plans are asked for. */
const DRIVING_DURATION_LIMIT = 6 * 60 * 60;
const MAP_URL = "https://www.google.com/maps/dir/?api=1";

type ConnectionType = "FERRY" | "CAR";

export interface Connection {
    id: string;
    origin: Location;
    destination: Location;
    /** Duration in seconds, or -1 for ferry connections, whose sailings each have their own. */
    duration: number;
    /** Distance in kilometers. */
    distance: number;
    /** Fuel usage in litres. For ferry connections, only that of boarding and unboarding. */
    fuel: number;
    type: ConnectionType;
}

export interface TimeInterval<Time = string> {
    start: Time;
    end: Time;
    description: string;
    /** `FREE` is extra time between segments, and `WAIT` is waiting at a terminal. */
    type: "FREE" | "WAIT" | "TRAVEL";
}

export interface RoutePlanSegment<Time = string> {
    connection: Connection;
    times: TimeInterval<Time>[];
    schedule_url?: string;
}

export interface RoutePlan {
    segments: RoutePlanSegment[];
    hash: string;
    /** Total duration in seconds. */
    duration: number;
    depart_time: string;
    arrive_time: string;
    /** Total driving duration in seconds. */
    driving_duration: number;
    /** Total driving distance in kilometers. */
    driving_distance: number;
    /** Google Maps URL of the route. */
    map_url: string;
}

export interface PlanOptions {
    /** Local time on the day to travel on. */
    date: number;
    showAll: boolean;
    assured: boolean;
    hostled: boolean;
    /** Buffer time in minutes. */
    buffer: number;
}

/** Segments use local times in milliseconds until their route plan is complete. */
type Segment = RoutePlanSegment<number>;

const connections = new Map<string, Connection | undefined>();
const connectionsFrom = new Map<LocationId, [LocationId, ConnectionType][]>();

const getConnection = (origin: LocationId, destination: LocationId): Connection | undefined => {
    const id = `${origin}-${destination}`;
    if (!connections.has(id)) {
        const car = carConnections[origin]?.[destination];
        const isFerry = ferryConnections[origin as TerminalId]?.[destination as TerminalId] !== undefined;
        const ends = { id, origin: locations[origin], destination: locations[destination] };
        connections.set(
            id,
            car
                ? { ...ends, ...car, type: "CAR" }
                : isFerry
                  ? { ...ends, duration: -1, distance: 0.2, fuel: 0.2, type: "FERRY" }
                  : undefined,
        );
    }
    return connections.get(id);
};

/** Get the destinations and types of the connections from a location, those by car first. */
const getConnectionsFrom = (origin: LocationId): [LocationId, ConnectionType][] => {
    let found = connectionsFrom.get(origin);
    if (!found) {
        found = [
            ...Object.keys(carConnections[origin] ?? {}).map((destination): [LocationId, ConnectionType] => [
                destination as LocationId,
                "CAR",
            ]),
            ...Object.keys(ferryConnections[origin as TerminalId] ?? {}).map(
                (destination): [LocationId, ConnectionType] => [destination as LocationId, "FERRY"],
            ),
        ];
        connectionsFrom.set(origin, found);
    }
    return found;
};

/** Find the routes between two locations, each as the locations it goes through. */
export const findRoutes = (origin: LocationId, destination: LocationId): LocationId[][] => {
    const routes: LocationId[][] = [];
    const route: LocationId[] = [];
    const deadEnds = new Set<string>();
    // Land groups left by ferry so far on the route, which are not returned to.
    const lands: string[] = [];
    const endsInCity = destination in cities;

    const follow = (point: LocationId, lastType?: ConnectionType): boolean => {
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

/** Find the ways to travel between two locations on a day, the shortest first. */
export const routePlans = (
    origin: LocationId,
    destination: LocationId,
    options: PlanOptions,
    timetable: Timetable,
    /** Current local time. */
    now: number,
): RoutePlan[] => {
    const plans: RoutePlan[] = [];
    for (const route of findRoutes(origin, destination)) {
        addSegment({
            plans,
            route,
            index: 1,
            segments: [],
            startTime: startOfDay(options.date),
            options,
            timetable,
            now,
        });
    }
    return plans.sort((a, b) => a.duration - b.duration);
};

interface PlanState {
    plans: RoutePlan[];
    route: LocationId[];
    /** Index in the route of the destination of the next segment. */
    index: number;
    segments: Segment[];
    startTime: number;
    options: PlanOptions;
    timetable: Timetable;
    now: number;
}

/** Add route plans for the rest of a route, and return whether there were any. */
const addSegment = (state: PlanState): boolean => {
    const { plans, route, index, segments, startTime, options } = state;
    const [origin, destination] = [route[index - 1], route[index]];
    try {
        if (!origin || !destination) {
            if (segments.length > 0) {
                plans.push(makeRoutePlan(segments, state.now));
            }
            return segments.length > 0;
        }
        const connection = getConnection(origin, destination);
        if (connection?.type === "FERRY") {
            return addFerrySegments(state, connection);
        }
        // Skip long drives.
        if (!connection || (!options.showAll && connection.duration > DRIVING_DURATION_LIMIT)) {
            return false;
        }
        const arriveTime = startTime + connection.duration * 1000;
        segments.push({
            connection,
            times: [
                {
                    type: "TRAVEL",
                    start: startTime,
                    end: arriveTime,
                    description: `Drive ${Math.round(connection.distance)} km to ${connection.destination.name}`,
                },
            ],
        });
        return addSegment({ ...state, index: index + 1, startTime: arriveTime });
    } finally {
        segments.length = Math.min(segments.length, index - 1);
    }
};

/** Add route plans for the rest of a route for each sailing that can be caught, and return whether there were any. */
const addFerrySegments = (state: PlanState, connection: Connection): boolean => {
    const { index, segments, startTime, options } = state;
    const origin = connection.origin as Terminal;
    const firstTime = segments[0]?.times[0]?.start ?? startTime;
    const day = startOfDay(startTime);
    const schedule = getSchedule(
        state.timetable,
        origin.id as TerminalId,
        connection.destination.id as TerminalId,
        day,
    );
    const bookable = ferryConnections[origin.id as TerminalId]?.[connection.destination.id as TerminalId]?.bookable;
    let found = false;
    for (const sailing of schedule.sailings) {
        const departTime = sailing.departure;
        // Only the time of day of the arrival is used, so sailings appear to take less than a day.
        let arriveTime = day + (sailing.arrival % MS_PER_DAY);
        if (arriveTime < departTime) {
            arriveTime += MS_PER_DAY;
        }
        // Skip routes that take more than one day.
        if ((!options.showAll && arriveTime - startTime > MS_PER_DAY) || day !== startOfDay(firstTime)) {
            break;
        }
        if (departTime < startTime) {
            continue;
        }
        let deadlineName = "departure";
        let waitMinutes = 0;
        if (options.hostled && origin.hostled_close) {
            deadlineName = "hostled vehicles check-in close";
            waitMinutes = origin.hostled_close;
        } else if (options.assured && origin.assured_close) {
            deadlineName = "assured loading check-in close";
            waitMinutes = origin.assured_close;
        } else if (origin.res_close && bookable) {
            deadlineName = "booking check-in close";
            waitMinutes = origin.res_close;
        } else if (origin.veh_close) {
            deadlineName = "vehicles check-in close";
            waitMinutes = origin.veh_close;
        } else if (origin.foot_close) {
            deadlineName = "foot passengers check-in close";
            waitMinutes = origin.foot_close;
        }
        const deadlineTime = departTime - (waitMinutes + options.buffer) * MS_PER_MINUTE;
        if (deadlineTime < startTime) {
            continue;
        }
        const times: Segment["times"] = [
            {
                type: "TRAVEL",
                start: departTime,
                end: arriveTime,
                description: `Ferry sailing from ${origin.name} to ${connection.destination.name}`,
            },
        ];
        if (deadlineTime < departTime) {
            const buffer = options.buffer > 0 ? `${options.buffer} minutes ` : "";
            times.unshift({
                type: "WAIT",
                start: deadlineTime,
                end: departTime,
                description: `Arrive at ${origin.name} ${buffer}before ${deadlineName}`,
            });
        }
        segments.push({ connection, times, schedule_url: schedule.url });
        if (!addSegment({ ...state, index: index + 1, startTime: arriveTime })) {
            break;
        }
        segments.length = index - 1;
        found = true;
        // After the first sailing of a route, only the first sailing that can be caught is taken.
        if (!options.showAll && segments.some((segment) => segment.connection.type === "FERRY")) {
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

const makeRoutePlan = (planSegments: Segment[], now: number): RoutePlan => {
    const segments = planSegments.map((segment) => ({
        ...segment,
        times: segment.times.map((time) => ({ ...time })),
    }));
    const first = segments[0];
    const last = segments.at(-1);
    if (!first || !last) {
        throw new Error("route plan must have at least one segment");
    }
    if (first.connection.type === "CAR") {
        const next = segments[1];
        // A drive at the start can be put off to arrive just in time for the ferry,
        // and a drive that is all there is starts at the current time of day.
        const shift = next
            ? (next.times[0]?.start ?? 0) - (first.times.at(-1)?.end ?? 0)
            : now - startOfDay(now) - (now % 1000);
        for (const time of first.times) {
            time.start += shift;
            time.end += shift;
        }
    }
    for (const [index, segment] of segments.entries()) {
        const freeStart = segment.times.at(-1)?.end;
        const freeEnd = segments[index + 1]?.times[0]?.start;
        if (freeStart !== undefined && freeEnd !== undefined && freeEnd > freeStart) {
            segment.times.push({ type: "FREE", start: freeStart, end: freeEnd, description: "Free time" });
        }
    }
    const departTime = first.times[0]?.start ?? 0;
    if (first.connection.type !== "FERRY") {
        first.times.unshift({
            type: "TRAVEL",
            start: departTime,
            end: departTime,
            description: `Depart from ${first.connection.origin.name}`,
        });
    }
    const arriveTime = last.times.at(-1)?.end ?? 0;
    last.times.push({
        type: "TRAVEL",
        start: arriveTime,
        end: arriveTime,
        description: `Arrive at ${last.connection.destination.name}`,
    });

    let drivingDuration = 0;
    let drivingDistance = 0;
    // Hashed the same way as by the Python planner before, so that links to route plans keep working.
    const hash = createHash("sha1");
    for (const segment of segments) {
        if (segment.connection.type === "CAR") {
            drivingDuration += segment.connection.duration;
            drivingDistance += segment.connection.distance;
        }
        hash.update(segment.connection.destination.id);
        for (const time of segment.times) {
            hash.update(formatLocal(time.start));
        }
    }
    const waypoints = segments.slice(1).map((segment) => mapParameter(segment.connection.origin));
    return {
        segments: segments.map((segment) => ({
            ...segment,
            times: segment.times.map((time) => ({
                ...time,
                start: formatLocal(time.start),
                end: formatLocal(time.end),
            })),
        })),
        hash: hash.digest("hex"),
        duration: (arriveTime - departTime) / 1000,
        depart_time: formatLocal(departTime),
        arrive_time: formatLocal(arriveTime),
        driving_duration: drivingDuration,
        driving_distance: drivingDistance,
        map_url:
            `${MAP_URL}&origin=${encodeURIComponent(mapParameter(first.connection.origin))}` +
            `&destination=${encodeURIComponent(mapParameter(last.connection.destination))}` +
            `&waypoints=${encodeURIComponent(waypoints.join("|"))}`,
    };
};
