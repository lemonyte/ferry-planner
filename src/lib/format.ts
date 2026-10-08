// Times are local to British Columbia and written as `YYYY-MM-DDTHH:MM:SS`.
// They are formatted by hand, as the server and the browser can format the same time differently.

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MS_PER_DAY = 24 * 60 * 60 * 1000;

/** Read a local time as if it were in UTC, to do arithmetic on it. */
const toDate = (time: string): Date => {
    return new Date(`${time.length > 10 ? time : `${time}T00:00:00`}Z`);
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
    // Rounded, so that it agrees with the times it is shown beside, which leave their seconds out.
    const minutes = Math.round(seconds / 60);
    const hours = Math.floor(minutes / 60);
    if (hours === 0) {
        return `${minutes} min`;
    }
    return minutes % 60 === 0 ? `${hours} h` : `${hours} h ${minutes % 60} min`;
};

/** Format a distance in kilometres, such as `144 km`. */
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
