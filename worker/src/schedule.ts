import { ferryConnections } from "./data/ferry-connections";
import { type TerminalId, terminals } from "./data/locations";
import type { Sailing, Timetable } from "./gtfs";
import { formatLocal, startOfDay, utcOffset } from "./time";

const SCHEDULE_BASE_URL = "https://www.bcferries.com/routes-fares/schedules/daily/";
const NO_SAILINGS_NOTE = "No sailings found";
const SCHEDULE_NOT_POSTED_NOTE = "Seasonal schedules have not been posted for these dates";

export interface Schedule {
    /** Local time that the schedule was asked for. */
    date: number;
    origin: TerminalId;
    destination: TerminalId;
    sailings: readonly Sailing[];
    url: string;
    /** Notes or comments posted about this schedule. */
    notes: string[];
}

/** Get the `[latitude, longitude]` of the terminals that have ferry connections, to match the stops of a feed to. */
export const terminalCoordinates = (): Record<string, [number, number]> => {
    const ids = new Set(
        Object.entries(ferryConnections).flatMap(([origin, destinations]) => [origin, ...Object.keys(destinations)]),
    );
    return Object.fromEntries(
        [...ids].map((id) => {
            const [latitude = Number.NaN, longitude = Number.NaN] = terminals[id as TerminalId].coordinates
                .split(",")
                .map(Number);
            return [id, [latitude, longitude]];
        }),
    );
};

/** Get the sailings between two terminals on the day of a local time. */
export const getSchedule = (
    timetable: Timetable,
    origin: TerminalId,
    destination: TerminalId,
    date: number,
): Schedule => {
    const day = startOfDay(date);
    // The feed can list sailings for dates it does not cover, but those are not reliable.
    const sailings = timetable.covers(day) ? timetable.sailings(origin, destination, day) : [];
    const [year, month, dayOfMonth] = formatLocal(day).slice(0, 10).split("-");
    return {
        date,
        origin,
        destination,
        sailings,
        url: `${SCHEDULE_BASE_URL}${origin}-${destination}?&scheduleDate=${month}/${dayOfMonth}/${year}`,
        notes: sailings.length > 0 ? [] : [timetable.covers(day) ? NO_SAILINGS_NOTE : SCHEDULE_NOT_POSTED_NOTE],
    };
};

/** Get the notes or comments posted about a sailing. */
export const sailingNotes = (sailing: Sailing): string[] => {
    return sailing.stops.length > 0
        ? [`Via ${sailing.stops.map((stop) => terminals[stop as TerminalId].name).join(", ")}`]
        : [];
};

/** Lay a schedule out the way the API gives it. */
export const scheduleResponse = (schedule: Schedule) => {
    return {
        date: formatLocal(schedule.date),
        origin: schedule.origin,
        destination: schedule.destination,
        sailings: schedule.sailings.map((sailing) => ({
            departure: formatLocal(sailing.departure) + utcOffset(sailing.departure),
            arrival: formatLocal(sailing.arrival) + utcOffset(sailing.arrival),
            /** Duration in seconds. */
            duration: (sailing.arrival - sailing.departure) / 1000,
            notes: sailingNotes(sailing),
        })),
        url: schedule.url,
        notes: schedule.notes,
    };
};
