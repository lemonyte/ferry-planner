// Times are local to British Columbia, written as `YYYY-MM-DDTHH:MM:SS`.
// Formatting is manual so that it does not depend on the time zone or locale of the device.

import { MS_PER_DAY, parseLocal } from "./planner/time.ts";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** Parse a local date or time as if it were UTC, for arithmetic. */
const toDate = (time: string): Date => {
    return new Date(parseLocal(time) ?? Number.NaN);
};

/** Format the time of day of a local time, such as `6:20 am`. */
export const formatTime = (time: string): string => {
    const date = toDate(time);
    const hours = date.getUTCHours();
    const minutes = String(date.getUTCMinutes()).padStart(2, "0");
    return `${hours % 12 || 12}:${minutes} ${hours < 12 ? "am" : "pm"}`;
};

/** Format the day of a local date or time, such as `Fri, Oct 9`. */
export const formatDay = (time: string): string => {
    const date = toDate(time);
    return `${WEEKDAYS[date.getUTCDay()]}, ${MONTHS[date.getUTCMonth()]} ${date.getUTCDate()}`;
};

/** Format a duration in seconds, such as `7 h 14 min`. */
export const formatDuration = (seconds: number): string => {
    // Rounded to match the times shown beside it, which omit seconds.
    const minutes = Math.round(seconds / 60);
    const hours = Math.floor(minutes / 60);
    if (hours === 0) {
        return `${minutes} min`;
    }
    return minutes % 60 === 0 ? `${hours} h` : `${hours} h ${minutes % 60} min`;
};

/** Format a distance in kilometers, such as `144 km`. */
export const formatDistance = (kilometres: number): string => {
    return `${Math.round(kilometres)} km`;
};

export const secondsBetween = (start: string, end: string): number => {
    return (toDate(end).getTime() - toDate(start).getTime()) / 1000;
};

/** Count the midnights between two local times. */
export const daysBetween = (start: string, end: string): number => {
    return (toDate(end.slice(0, 10)).getTime() - toDate(start.slice(0, 10)).getTime()) / MS_PER_DAY;
};

/** Add days to a local date written as `YYYY-MM-DD`. */
export const addDays = (date: string, days: number): string => {
    return new Date(toDate(date).getTime() + days * MS_PER_DAY).toISOString().slice(0, 10);
};
