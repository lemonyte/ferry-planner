import { ferryConnections } from "./data/ferry-connections.ts";
import { type TerminalId, terminals } from "./data/locations.ts";
import type { Sailing, Timetable } from "./gtfs.ts";
import { formatLocal, startOfDay } from "./time.ts";

const SCHEDULE_BASE_URL = "https://www.bcferries.com/routes-fares/schedules/daily/";

export interface Schedule {
    sailings: readonly Sailing[];
    /** URL of the schedule on the BC Ferries website. */
    url: string;
}

/** Get the `[latitude, longitude]` of each terminal with a ferry connection, to match feed stops to. */
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
    // The feed can list sailings for dates outside its date range, but they are not reliable.
    const sailings = timetable.covers(day) ? timetable.sailings(origin, destination, day) : [];
    const [year, month, dayOfMonth] = formatLocal(day).slice(0, 10).split("-");
    return {
        sailings,
        url: `${SCHEDULE_BASE_URL}${origin}-${destination}?&scheduleDate=${month}/${dayOfMonth}/${year}`,
    };
};
