// Local times are held in milliseconds as if they were UTC, which keeps arithmetic on them clear of time zones.
// The Workers runtime itself always runs in UTC.

export const MS_PER_MINUTE = 60 * 1000;
export const MS_PER_DAY = 24 * 60 * MS_PER_MINUTE;

const TIMEZONE = "America/Vancouver";
const OFFSET_FORMAT = new Intl.DateTimeFormat("en-US", { timeZone: TIMEZONE, timeZoneName: "longOffset" });

/** Format a local time as `YYYY-MM-DDTHH:MM:SS`. */
export const formatLocal = (time: number): string => {
    return new Date(time).toISOString().slice(0, 19);
};

/** Parse a local date or date and time in ISO 8601 format, reading it as written whatever UTC offset it gives. */
export const parseLocal = (value: string): number | undefined => {
    const match = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?/.exec(value);
    if (!match) {
        return undefined;
    }
    const [year, month, day, hour = 0, minute = 0, second = 0] = match.slice(1).map((part) => Number(part ?? 0));
    const time = Date.UTC(year ?? 0, (month ?? 1) - 1, day, hour, minute, second);
    // Dates that do not exist, such as the 31st of June, would otherwise roll over into the next month.
    return formatLocal(time).startsWith(value.slice(0, 10)) ? time : undefined;
};

export const startOfDay = (time: number): number => {
    return time - (((time % MS_PER_DAY) + MS_PER_DAY) % MS_PER_DAY);
};

/** Get the UTC offset in effect at an instant, such as `-07:00`. */
const utcOffsetAt = (instant: number): string => {
    const name = OFFSET_FORMAT.formatToParts(instant).find((part) => part.type === "timeZoneName")?.value ?? "";
    // The name is `GMT-07:00`, or `GMT` alone for no offset.
    return name.slice(3) || "+00:00";
};

const offsetMs = (offset: string): number => {
    const [hours = 0, minutes = 0] = offset.slice(1).split(":").map(Number);
    return (offset.startsWith("-") ? -1 : 1) * (hours * 60 + minutes) * MS_PER_MINUTE;
};

/** Get the UTC offset in effect at a local time, such as `-07:00`. */
export const utcOffset = (time: number): string => {
    // The offset at the instant read as UTC is right except within hours of a clock change.
    return utcOffsetAt(time - offsetMs(utcOffsetAt(time)));
};

/** Convert an instant, such as `Date.now()`, to the local time. */
export const toLocal = (instant: number): number => {
    return instant + offsetMs(utcOffsetAt(instant));
};
