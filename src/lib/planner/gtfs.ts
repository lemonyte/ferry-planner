import { unzipSync } from "fflate";

import { cached } from "./cache.ts";
import { MS_PER_DAY } from "./time.ts";

/**
 * Maximum distance between a stop and a location for the stop to match it.
 *
 * Less than half the distance between the two closest terminals, so no stop matches two terminals.
 */
const MAX_STOP_DISTANCE_KM = 0.5;
/**
 * Maximum time that a vessel stays at an intermediate terminal.
 *
 * The feed does not identify vessels, so two trips of a route are treated as one vessel if the second
 * departs from the destination of the first within this time.
 */
const MAX_CALL_SECONDS = 20 * 60;
const KM_PER_DEGREE = 111.2;
const WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] as const;
const SERVICE_ADDED = "1";
const NOT_AVAILABLE = "1";
const SECONDS_PER_DAY = 24 * 60 * 60;
const FILES = ["stops.txt", "feed_info.txt", "trips.txt", "calendar.txt", "calendar_dates.txt", "stop_times.txt"];

/**
 * Part of a trip between two consecutive locations.
 *
 * Times are in seconds since the start of the service day.
 */
export interface Leg {
    departure: number;
    arrival: number;
    origin: string;
    destination: string;
    trip: string;
    /** Route of the trip. A vessel stays on one route. */
    route: string;
    canBoard: boolean;
    canAlight: boolean;
    /** Services that define when the trip runs. The first service with an entry for a date decides. */
    services: string[];
}

/** Sailings from a GTFS feed archive, as JSON-serializable data. */
export interface Feed {
    /** Date range that the feed covers, as `YYYYMMDD`, if the feed gives one. */
    startDate?: string;
    endDate?: string;
    legs: Leg[];
    /** Weekdays from Monday and `YYYYMMDD` date range that each service runs on. */
    calendar: Record<string, { weekdays: boolean[]; startDate: string; endDate: string }>;
    /** Dates that a service is added to (`true`) or removed from (`false`), by service then `YYYYMMDD`. */
    calendarDates: Record<string, Record<string, boolean>>;
    /** Locations with no sailings in the feed. */
    unserved: string[];
}

/** Times are local, in milliseconds as if the local time were UTC. */
export interface Sailing {
    departure: number;
    arrival: number;
    /** IDs of the intermediate locations. */
    stops: string[];
}

type Row = Record<string, string | undefined>;

/** Stop of a trip at a location, with times in seconds since the start of the service day. */
interface Call {
    sequence: number;
    location: string;
    arrival: number;
    departure: number;
    canBoard: boolean;
    canAlight: boolean;
}

/**
 * Parse a GTFS feed archive.
 *
 * Stops are matched to the nearest of `locations`, which maps location IDs to `[latitude, longitude]`.
 */
export const parseFeed = (data: Uint8Array, locations: Record<string, [number, number]>): Feed => {
    const archive = unzipSync(data, { filter: (file) => FILES.includes(file.name) });
    const stopLocations = new Map(
        readTable(archive, "stops.txt").flatMap((row): [string, string | undefined][] =>
            // Stops that are not boarding points, such as entrances, can lack coordinates.
            row.stop_lat && row.stop_lon
                ? [
                      [
                          required(row, "stop_id"),
                          nearestLocation(parseNumber(row.stop_lat), parseNumber(row.stop_lon), locations),
                      ],
                  ]
                : [],
        ),
    );
    const feedInfo = readTable(archive, "feed_info.txt", true)[0];
    const trips = new Map(
        readTable(archive, "trips.txt").map((row) => [
            required(row, "trip_id"),
            { service: required(row, "service_id"), route: required(row, "route_id") },
        ]),
    );
    const calendar: Feed["calendar"] = Object.fromEntries(
        readTable(archive, "calendar.txt", true).map((row) => [
            required(row, "service_id"),
            {
                weekdays: WEEKDAYS.map((weekday) => required(row, weekday) === "1"),
                startDate: parseDate(row.start_date),
                endDate: parseDate(row.end_date),
            },
        ]),
    );
    const calendarDates: Feed["calendarDates"] = {};
    for (const row of readTable(archive, "calendar_dates.txt", true)) {
        const service = required(row, "service_id");
        const dates = calendarDates[service] ?? {};
        calendarDates[service] = dates;
        dates[parseDate(row.date)] = row.exception_type === SERVICE_ADDED;
    }
    const tripCalls = new Map<string, Call[]>();
    for (const row of readTable(archive, "stop_times.txt")) {
        const location = stopLocations.get(required(row, "stop_id"));
        // Each time defaults to the other. Stops that a trip only passes can have neither.
        const arrival = row.arrival_time || row.departure_time;
        const departure = row.departure_time || row.arrival_time;
        if (location && arrival && departure) {
            const tripId = required(row, "trip_id");
            const calls = tripCalls.get(tripId) ?? [];
            tripCalls.set(tripId, calls);
            calls.push({
                sequence: parseInteger(row.stop_sequence),
                location,
                arrival: parseSeconds(arrival),
                departure: parseSeconds(departure),
                canBoard: row.pickup_type !== NOT_AVAILABLE,
                canAlight: row.drop_off_type !== NOT_AVAILABLE,
            });
        }
    }
    const legs = [...tripCalls].flatMap(([trip, calls]): Leg[] => {
        const { service, route } = trips.get(trip) ?? {};
        if (service === undefined || route === undefined) {
            throw new Error(`trip ${trip} has stop times but no service`);
        }
        const sorted = calls.toSorted((a, b) => a.sequence - b.sequence);
        return sorted.flatMap((call, index) => {
            const nextCall = sorted[index + 1];
            return nextCall && call.location !== nextCall.location
                ? [
                      {
                          departure: call.departure,
                          arrival: nextCall.arrival,
                          origin: call.location,
                          destination: nextCall.location,
                          trip,
                          route,
                          canBoard: call.canBoard,
                          canAlight: nextCall.canAlight,
                          // The BC Ferries feed lists dates added to or removed from a single trip under a service
                          // named `{service}{trip}`, which takes priority over the service of the trip.
                          services: [service + trip, service],
                      },
                  ]
                : [];
        });
    });
    const served = new Set(legs.flatMap((leg) => [leg.origin, leg.destination]));
    return {
        startDate: feedInfo?.feed_start_date ? parseDate(feedInfo.feed_start_date) : undefined,
        endDate: feedInfo?.feed_end_date ? parseDate(feedInfo.feed_end_date) : undefined,
        legs,
        calendar,
        calendarDates,
        unserved: Object.keys(locations)
            .filter((location) => !served.has(location))
            .sort(),
    };
};

/** Looks up sailings in a feed by location ID. */
export class Timetable {
    // Cache of sailings by origin, destination, and date. The route planner repeats the same lookups many times.
    private readonly found = new Map<string, Sailing[]>();
    // Cache of the legs that run on each service day, by origin.
    private readonly running = new Map<number, Map<string, Leg[]>>();

    constructor(readonly feed: Feed) {}

    /** Check if the feed covers a date, given as the local time at the start of the day. */
    covers(date: number): boolean {
        const day = formatDate(date);
        return (!this.feed.startDate || this.feed.startDate <= day) && (!this.feed.endDate || day <= this.feed.endDate);
    }

    /** Get the sailings between two locations on a date, given as the local time at the start of the day. */
    sailings(origin: string, destination: string, date: number): readonly Sailing[] {
        return cached(this.found, `${origin}-${destination}-${date}`, () =>
            this.findSailings(origin, destination, date),
        );
    }

    private findSailings(origin: string, destination: string, date: number): Sailing[] {
        const sailings = new Map<string, Sailing>();
        // Sailings that depart after midnight belong to the service day before.
        for (const daysBefore of [0, 1]) {
            const serviceDate = date - daysBefore * MS_PER_DAY;
            for (const [departure, arrival, stops] of findJourneys(this.legsFrom(serviceDate), origin, destination)) {
                if (Math.floor(departure / SECONDS_PER_DAY) === daysBefore) {
                    const sailing = {
                        departure: serviceDate + departure * 1000,
                        arrival: serviceDate + arrival * 1000,
                        stops,
                    };
                    // The same sailing can be listed under more than one trip.
                    sailings.set(`${sailing.departure} ${sailing.arrival} ${stops.join(",")}`, sailing);
                }
            }
        }
        return [...sailings.values()].sort(
            (a, b) => a.departure - b.departure || a.arrival - b.arrival || compareStops(a.stops, b.stops),
        );
    }

    /** Get the legs that run on a service day, by origin. */
    private legsFrom(serviceDate: number): Map<string, Leg[]> {
        return cached(this.running, serviceDate, () => {
            const day = formatDate(serviceDate);
            // `getUTCDay()` counts from Sunday, and the calendar from Monday.
            const weekday = (new Date(serviceDate).getUTCDay() + 6) % 7;
            return Map.groupBy(
                this.feed.legs.filter((leg) => this.runsOn(leg.services, day, weekday)),
                (leg) => leg.origin,
            );
        });
    }

    /** Check if a trip runs on a date. The first of its services with an entry for the date decides. */
    private runsOn(services: string[], day: string, weekday: number): boolean {
        for (const service of services) {
            const added = this.feed.calendarDates[service]?.[day];
            if (added !== undefined) {
                return added;
            }
        }
        for (const service of services) {
            const calendar = this.feed.calendar[service];
            if (calendar) {
                return calendar.weekdays[weekday] === true && calendar.startDate <= day && day <= calendar.endDate;
            }
        }
        return false;
    }
}

const readTable = (archive: Record<string, Uint8Array>, name: string, optional = false): Row[] => {
    const file = archive[name];
    if (!file) {
        if (optional) {
            return [];
        }
        throw new Error(`${name} is missing`);
    }
    const [columns = [], ...records] = parseCsv(new TextDecoder().decode(file));
    return records.map((record) => Object.fromEntries(columns.map((column, index) => [column, record[index]])));
};

/** Parse the records of a CSV file, in which values with commas, quotes, or line breaks are quoted. */
const parseCsv = (text: string): string[][] => {
    const records: string[][] = [];
    let record: string[] = [];
    let value = "";
    // Copies each run of plain text whole, which is much faster than copying it a character at a time.
    const special = /[",\n\r]/g;
    let index = 0;
    while (index < text.length) {
        special.lastIndex = index;
        const match = special.exec(text);
        const end = match?.index ?? text.length;
        value += text.slice(index, end);
        index = end + 1;
        const character = match?.[0];
        if (character === '"') {
            // Copy up to the closing quote, or to the end of an unclosed value. Two quotes in a row stand for one.
            let close = text.indexOf('"', index);
            while (close !== -1 && text[close + 1] === '"') {
                value += text.slice(index, close + 1);
                index = close + 2;
                close = text.indexOf('"', index);
            }
            value += text.slice(index, close === -1 ? text.length : close);
            index = close === -1 ? text.length : close + 1;
        } else if (character === ",") {
            record.push(value);
            value = "";
        } else if (character === "\n") {
            record.push(value);
            value = "";
            // Skip empty lines.
            if (record.length > 1 || record[0] !== "") {
                records.push(record);
            }
            record = [];
        }
        // A `\r` outside quotes is dropped.
    }
    if (value !== "" || record.length > 0) {
        records.push([...record, value]);
    }
    return records;
};

const required = (row: Row, column: string): string => {
    const value = row[column];
    if (value === undefined) {
        throw new Error(`row has no ${column}`);
    }
    return value;
};

const parseInteger = (value: string | undefined): number => {
    if (!value || !/^\d+$/.test(value)) {
        throw new Error(`${value} is not a whole number`);
    }
    return Number(value);
};

const parseNumber = (value: string): number => {
    const number = Number(value);
    if (!Number.isFinite(number)) {
        throw new Error(`${value} is not a number`);
    }
    return number;
};

const parseDate = (value: string | undefined): string => {
    if (!value || !/^\d{8}$/.test(value)) {
        throw new Error(`${value} is not a date`);
    }
    return value;
};

/** Parse a `HH:MM:SS` time, which can be past 24:00:00 for trips that run over midnight. */
const parseSeconds = (value: string): number => {
    const [hours, minutes, seconds, ...rest] = value.split(":").map(parseInteger);
    if (hours === undefined || minutes === undefined || seconds === undefined || rest.length > 0) {
        throw new Error(`${value} is not a time`);
    }
    return hours * 3600 + minutes * 60 + seconds;
};

const formatDate = (date: number): string => {
    return new Date(date).toISOString().slice(0, 10).replaceAll("-", "");
};

const nearestLocation = (
    latitude: number,
    longitude: number,
    locations: Record<string, [number, number]>,
): string | undefined => {
    let nearest: string | undefined;
    let nearestDistance = MAX_STOP_DISTANCE_KM / KM_PER_DEGREE;
    for (const [location, [locationLatitude, locationLongitude]] of Object.entries(locations)) {
        const distance = Math.hypot(
            latitude - locationLatitude,
            (longitude - locationLongitude) * Math.cos((latitude * Math.PI) / 180),
        );
        if (distance <= nearestDistance && (nearest === undefined || distance < nearestDistance)) {
            nearest = location;
            nearestDistance = distance;
        }
    }
    return nearest;
};

const compareStops = (a: string[], b: string[]): number => {
    for (const [index, stop] of a.entries()) {
        const other = b[index];
        if (other === undefined || stop > other) {
            return 1;
        }
        if (stop < other) {
            return -1;
        }
    }
    return a.length - b.length;
};

/**
 * Find the departure, arrival, and intermediate stops of the sailings between two locations on a service day.
 *
 * The BC Ferries feed lists each part of a multi-stop sailing as a separate trip, so a sailing can span
 * several trips. Trips on different vessels are not joined, because changing vessels makes two sailings.
 */
const findJourneys = (
    legsFrom: Map<string, Leg[]>,
    origin: string,
    destination: string,
): [departure: number, arrival: number, stops: string[]][] => {
    // Journeys by departure and arrival, keeping the one with the fewest stops.
    const journeys = new Map<string, [number, number, string[]]>();
    for (const firstLeg of legsFrom.get(origin) ?? []) {
        const path = fastestPath(firstLeg, destination, legsFrom);
        const lastLeg = path.at(-1);
        if (lastLeg) {
            const key = `${firstLeg.departure} ${lastLeg.arrival}`;
            const stops = path.slice(0, -1).map((leg) => leg.destination);
            const other = journeys.get(key)?.[2];
            if (
                !other ||
                stops.length < other.length ||
                (stops.length === other.length && compareStops(stops, other) < 0)
            ) {
                journeys.set(key, [firstLeg.departure, lastLeg.arrival, stops]);
            }
        }
    }
    return [...journeys.values()];
};

/** Find the legs of one vessel that reach a destination earliest after a first leg. */
const fastestPath = (firstLeg: Leg, destination: string, legsFrom: Map<string, Leg[]>): Leg[] => {
    if (!firstLeg.canBoard) {
        return [];
    }
    const previousLegs = new Map<Leg, Leg | undefined>([[firstLeg, undefined]]);
    let lastLeg: Leg | undefined;
    const queue = [firstLeg];
    for (const leg of queue) {
        if (leg.destination === destination) {
            if (leg.canAlight && (!lastLeg || leg.arrival < lastLeg.arrival)) {
                lastLeg = leg;
            }
            // Returning to the origin only gives a slower version of a later sailing.
        } else if (leg.destination !== firstLeg.origin) {
            for (const nextLeg of legsFrom.get(leg.destination) ?? []) {
                const wait = nextLeg.departure - leg.arrival;
                const canContinue =
                    nextLeg.trip === leg.trip
                        ? wait >= 0
                        : nextLeg.route === leg.route && wait >= 0 && wait <= MAX_CALL_SECONDS;
                if (canContinue && !previousLegs.has(nextLeg)) {
                    previousLegs.set(nextLeg, leg);
                    queue.push(nextLeg);
                }
            }
        }
    }
    const path: Leg[] = [];
    while (lastLeg) {
        path.push(lastLeg);
        lastLeg = previousLegs.get(lastLeg);
    }
    return path.reverse();
};
