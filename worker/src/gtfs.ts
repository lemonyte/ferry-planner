import { unzipSync } from "fflate";

/**
 * Stops further than this from every location are ignored.
 *
 * Less than half the distance between the two terminals closest to each other, so no stop is near two of them.
 */
const MAX_STOP_DISTANCE_KM = 0.5;
/** Longest wait between two trips of a sailing. */
const MAX_TRANSFER_SECONDS = 2 * 60 * 60;
const KM_PER_DEGREE = 111.2;
const WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] as const;
const SERVICE_ADDED = "1";
const NOT_AVAILABLE = "1";
const SECONDS_PER_DAY = 24 * 60 * 60;
const MS_PER_DAY = SECONDS_PER_DAY * 1000;
const FILES = [
    "stops.txt",
    "feed_info.txt",
    "trips.txt",
    "calendar.txt",
    "calendar_dates.txt",
    "transfers.txt",
    "stop_times.txt",
];

/**
 * Part of a trip between two locations that it calls at one after the other.
 *
 * Times are in seconds since the start of the service day.
 */
export interface Leg {
    departure: number;
    arrival: number;
    origin: string;
    destination: string;
    trip: string;
    canBoard: boolean;
    canAlight: boolean;
    /** Services that say when the trip runs, the first that says anything about a date deciding. */
    services: string[];
}

/** Sailings from a GTFS feed archive, as plain data that can be stored and read back. */
export interface Feed {
    /** Date range that the feed has schedules for, as `YYYYMMDD`, if it says so. */
    startDate?: string;
    endDate?: string;
    legs: Leg[];
    /** Weekdays from Monday and `YYYYMMDD` date range that each service runs on. */
    calendar: Record<string, { weekdays: boolean[]; startDate: string; endDate: string }>;
    /** Whether a service is added to or removed from a date regardless of its calendar, by service then `YYYYMMDD`. */
    calendarDates: Record<string, Record<string, boolean>>;
    /** Shortest time to change trips in at each location that has one. */
    transferSeconds: Record<string, number>;
    /** Locations that the feed has no sailings for. */
    unserved: string[];
}

/** Times are local, in milliseconds as if the local time were UTC. */
export interface Sailing {
    departure: number;
    arrival: number;
    /** IDs of the locations that the sailing calls at on the way. */
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
    const stopLocations = new Map<string, string | undefined>();
    for (const row of readTable(archive, "stops.txt")) {
        // Stops that are not boarded at, such as entrances, can have no coordinates.
        if (row.stop_lat && row.stop_lon) {
            stopLocations.set(
                required(row, "stop_id"),
                nearestLocation(parseNumber(row.stop_lat), parseNumber(row.stop_lon), locations),
            );
        }
    }
    const feedInfo = readTable(archive, "feed_info.txt", true)[0];
    const tripServices = new Map(
        readTable(archive, "trips.txt").map((row) => [required(row, "trip_id"), required(row, "service_id")]),
    );
    const calendar: Feed["calendar"] = {};
    for (const row of readTable(archive, "calendar.txt", true)) {
        calendar[required(row, "service_id")] = {
            weekdays: WEEKDAYS.map((weekday) => required(row, weekday) === "1"),
            startDate: parseDate(row.start_date),
            endDate: parseDate(row.end_date),
        };
    }
    const calendarDates: Feed["calendarDates"] = {};
    for (const row of readTable(archive, "calendar_dates.txt", true)) {
        const service = required(row, "service_id");
        const dates = calendarDates[service] ?? {};
        calendarDates[service] = dates;
        dates[parseDate(row.date)] = row.exception_type === SERVICE_ADDED;
    }
    const transferSeconds: Feed["transferSeconds"] = {};
    for (const row of readTable(archive, "transfers.txt", true)) {
        const location = stopLocations.get(required(row, "from_stop_id"));
        if (location && location === stopLocations.get(required(row, "to_stop_id")) && row.min_transfer_time) {
            transferSeconds[location] = Math.max(transferSeconds[location] ?? 0, parseInteger(row.min_transfer_time));
        }
    }
    const tripCalls = new Map<string, Call[]>();
    for (const row of readTable(archive, "stop_times.txt")) {
        const location = stopLocations.get(required(row, "stop_id"));
        // Either time stands in for the other, and stops that are only passed can have neither.
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
    const legs: Leg[] = [];
    for (const [trip, calls] of tripCalls) {
        const service = tripServices.get(trip);
        if (service === undefined) {
            throw new Error(`trip ${trip} has stop times but no service`);
        }
        calls.sort((a, b) => a.sequence - b.sequence);
        for (const [index, call] of calls.entries()) {
            const nextCall = calls[index + 1];
            if (nextCall && call.location !== nextCall.location) {
                legs.push({
                    departure: call.departure,
                    arrival: nextCall.arrival,
                    origin: call.location,
                    destination: nextCall.location,
                    trip,
                    canBoard: call.canBoard,
                    canAlight: nextCall.canAlight,
                    // The BC Ferries feed lists the dates that a single trip is added to or removed from
                    // under a service named after both the trip's service and the trip,
                    // which takes priority over the trip's service.
                    services: [service + trip, service],
                });
            }
        }
    }
    const served = new Set(legs.flatMap((leg) => [leg.origin, leg.destination]));
    return {
        startDate: feedInfo?.feed_start_date ? parseDate(feedInfo.feed_start_date) : undefined,
        endDate: feedInfo?.feed_end_date ? parseDate(feedInfo.feed_end_date) : undefined,
        legs,
        calendar,
        calendarDates,
        transferSeconds,
        unserved: Object.keys(locations)
            .filter((location) => !served.has(location))
            .sort(),
    };
};

/** Looks up sailings in a feed by the IDs of the locations nearest to the feed's stops. */
export class Timetable {
    // Sailings that have been looked up, as the route planner asks for the same ones many times over.
    private readonly found = new Map<string, readonly Sailing[]>();
    // Legs that run on each service day that has been looked up, by origin.
    private readonly running = new Map<number, Map<string, Leg[]>>();

    constructor(readonly feed: Feed) {}

    /** Check if the feed has schedules for a date, given as the local time at the start of the day. */
    covers(date: number): boolean {
        const day = formatDate(date);
        return (
            (!this.feed.startDate || this.feed.startDate <= day) && (!this.feed.endDate || day <= this.feed.endDate)
        );
    }

    /** Get the sailings departing from a location on a date, given as the local time at the start of the day. */
    sailings(origin: string, destination: string, date: number): readonly Sailing[] {
        const key = `${origin}-${destination}-${date}`;
        let sailings = this.found.get(key);
        if (!sailings) {
            sailings = this.findSailings(origin, destination, date);
            this.found.set(key, sailings);
        }
        return sailings;
    }

    private findSailings(origin: string, destination: string, date: number): Sailing[] {
        const sailings = new Map<string, Sailing>();
        // Sailings that depart past midnight are listed under the day before, which is their service day.
        for (const daysBefore of [0, 1]) {
            const serviceDate = date - daysBefore * MS_PER_DAY;
            for (const [departure, arrival, stops] of findJourneys(
                this.legsFrom(serviceDate),
                origin,
                destination,
                this.feed.transferSeconds,
            )) {
                if (Math.floor(departure / SECONDS_PER_DAY) === daysBefore) {
                    const sailing = {
                        departure: serviceDate + departure * 1000,
                        arrival: serviceDate + arrival * 1000,
                        stops,
                    };
                    // The same sailing can be listed under more than one trip.
                    sailings.set(`${sailing.departure} ${sailing.arrival} ${stops}`, sailing);
                }
            }
        }
        return [...sailings.values()].sort(
            (a, b) => a.departure - b.departure || a.arrival - b.arrival || compareStops(a.stops, b.stops),
        );
    }

    private legsFrom(serviceDate: number): Map<string, Leg[]> {
        let legsFrom = this.running.get(serviceDate);
        if (!legsFrom) {
            legsFrom = new Map();
            const day = formatDate(serviceDate);
            // Days are counted from Sunday, and the calendar's from Monday.
            const weekday = (new Date(serviceDate).getUTCDay() + 6) % 7;
            for (const leg of this.feed.legs) {
                if (this.runsOn(leg.services, day, weekday)) {
                    const legs = legsFrom.get(leg.origin) ?? [];
                    legsFrom.set(leg.origin, legs);
                    legs.push(leg);
                }
            }
            this.running.set(serviceDate, legsFrom);
        }
        return legsFrom;
    }

    /** Check if the first of the services that says anything about a date runs on it. */
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
    let quoted = false;
    for (let index = 0; index < text.length; index++) {
        const character = text[index];
        if (quoted) {
            if (character !== '"') {
                value += character;
            } else if (text[index + 1] === '"') {
                value += '"';
                index++;
            } else {
                quoted = false;
            }
        } else if (character === '"') {
            quoted = true;
        } else if (character === ",") {
            record.push(value);
            value = "";
        } else if (character === "\n") {
            record.push(value);
            value = "";
            // Lines without anything on them are not records.
            if (record.length > 1 || record[0] !== "") {
                records.push(record);
            }
            record = [];
        } else if (character !== "\r") {
            value += character;
        }
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
 * Find the departure, arrival, and stops on the way of the sailings between two locations on a service day.
 *
 * The BC Ferries feed lists each part of a sailing that calls at several terminals as a trip of its own,
 * the same as a sailing that connects with another, so a sailing can be made of several trips.
 */
const findJourneys = (
    legsFrom: Map<string, Leg[]>,
    origin: string,
    destination: string,
    transferSeconds: Record<string, number>,
): [departure: number, arrival: number, stops: string[]][] => {
    // Departure, arrival, number of transfers, and stops on the way, for each departure and arrival.
    const journeys = new Map<string, [number, number, number, string[]]>();
    for (const firstLeg of legsFrom.get(origin) ?? []) {
        const path = fastestPath(firstLeg, destination, legsFrom, transferSeconds);
        const lastLeg = path.at(-1);
        if (lastLeg) {
            const key = `${firstLeg.departure} ${lastLeg.arrival}`;
            const transfers = path.filter((leg, index) => index > 0 && leg.trip !== path[index - 1]?.trip).length;
            const stops = path.slice(0, -1).map((leg) => leg.destination);
            const other = journeys.get(key);
            if (!other || transfers < other[2] || (transfers === other[2] && compareStops(stops, other[3]) < 0)) {
                journeys.set(key, [firstLeg.departure, lastLeg.arrival, transfers, stops]);
            }
        }
    }
    const found = [...journeys.values()];
    return (
        found
            // Changing trips is only worth it when no later sailing arrives as early.
            .filter(
                ([departure, arrival, transfers]) =>
                    !transfers ||
                    !found.some(
                        ([otherDeparture, otherArrival]) =>
                            otherDeparture >= departure &&
                            otherArrival <= arrival &&
                            (otherDeparture !== departure || otherArrival !== arrival),
                    ),
            )
            .map(([departure, arrival, , stops]) => [departure, arrival, stops])
    );
};

/** Find the legs that arrive at a destination the earliest after a first leg, with as few legs as possible. */
const fastestPath = (
    firstLeg: Leg,
    destination: string,
    legsFrom: Map<string, Leg[]>,
    transferSeconds: Record<string, number>,
): Leg[] => {
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
            // Returning to the origin only makes for a slower version of a later sailing.
        } else if (leg.destination !== firstLeg.origin) {
            for (const nextLeg of legsFrom.get(leg.destination) ?? []) {
                const wait = nextLeg.departure - leg.arrival;
                const canContinue =
                    nextLeg.trip === leg.trip
                        ? wait >= 0
                        : leg.canAlight &&
                          nextLeg.canBoard &&
                          (transferSeconds[leg.destination] ?? 0) <= wait &&
                          wait <= MAX_TRANSFER_SECONDS;
                if (canContinue && !previousLegs.has(nextLeg)) {
                    previousLegs.set(nextLeg, leg);
                    queue.push(nextLeg);
                }
            }
        }
    }
    const path: Leg[] = [];
    while (lastLeg) {
        path.unshift(lastLeg);
        lastLeg = previousLegs.get(lastLeg);
    }
    return path;
};
