import { strToU8, zipSync } from "fflate";

export const LOCATIONS: Record<string, [number, number]> = {
    HSB: [49.3771, -123.2715],
    LNG: [49.434, -123.472],
    NAN: [49.1935, -123.9547],
};
export const EVERY_DAY = "daily,1,1,1,1,1,1,1,20260101,20261231";
export const STOPS = `stop_id,stop_name,stop_lat,stop_lon
1,Horseshoe Bay,49.3770,-123.2716
2,Langdale,49.4341,-123.4721
3,Departure Bay,49.1936,-123.9548
`;
export const HSB_TO_LNG = "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:10:00,2,2\n";
export const STOP_TIMES_COLUMNS = "trip_id,arrival_time,departure_time,stop_id,stop_sequence";

export interface FeedFiles {
    calendar?: string | null;
    calendarDates?: string | null;
    trips?: string;
    stopTimes?: string;
    stopTimesColumns?: string;
    stops?: string;
    feedInfo?: string;
    transfers?: string;
}

/**
 * Build a GTFS feed archive, by default with a single trip `t` that runs every day on service `daily`.
 *
 * Files given as `null` are left out of the archive.
 */
export const makeArchive = ({
    calendar = EVERY_DAY,
    calendarDates = "",
    trips = "r,daily,t\n",
    stopTimes = HSB_TO_LNG,
    stopTimesColumns = STOP_TIMES_COLUMNS,
    stops = STOPS,
    feedInfo,
    transfers,
}: FeedFiles = {}): Uint8Array => {
    const files: Record<string, string> = {
        "stops.txt": stops,
        "trips.txt": `route_id,service_id,trip_id\n${trips}`,
        "stop_times.txt": `${stopTimesColumns}\n${stopTimes}`,
    };
    if (calendar !== null) {
        files["calendar.txt"] =
            `service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n${calendar}\n`;
    }
    if (calendarDates !== null) {
        files["calendar_dates.txt"] = `service_id,date,exception_type\n${calendarDates}`;
    }
    if (feedInfo !== undefined) {
        files["feed_info.txt"] = `feed_publisher_name,feed_start_date,feed_end_date\n${feedInfo}\n`;
    }
    if (transfers !== undefined) {
        files["transfers.txt"] = `from_stop_id,to_stop_id,transfer_type,min_transfer_time\n${transfers}`;
    }
    return zipSync(Object.fromEntries(Object.entries(files).map(([name, content]) => [name, strToU8(content)])));
};
