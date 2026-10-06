from __future__ import annotations

import io
import zipfile
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("America/Vancouver")
LOCATIONS = {
    "HSB": (49.3771, -123.2715),
    "LNG": (49.4340, -123.4720),
    "NAN": (49.1935, -123.9547),
}
EVERY_DAY = "daily,1,1,1,1,1,1,1,20260101,20261231"
STOPS = """\
stop_id,stop_name,stop_lat,stop_lon
1,Horseshoe Bay,49.3770,-123.2716
2,Langdale,49.4341,-123.4721
3,Departure Bay,49.1936,-123.9548
"""
HSB_TO_LNG = "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:10:00,2,2\n"


def make_archive(
    *,
    calendar: str = EVERY_DAY,
    calendar_dates: str = "",
    trips: str = "r,daily,t\n",
    stop_times: str = HSB_TO_LNG,
    stops: str = STOPS,
    feed_info: str | None = None,
) -> bytes:
    """Build a GTFS feed archive, by default with a single trip `t` that runs every day on service `daily`."""
    files = {
        "stops.txt": stops,
        "trips.txt": f"route_id,service_id,trip_id\n{trips}",
        "calendar.txt": (
            f"service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n{calendar}\n"
        ),
        "calendar_dates.txt": f"service_id,date,exception_type\n{calendar_dates}",
        "stop_times.txt": f"trip_id,arrival_time,departure_time,stop_id,stop_sequence\n{stop_times}",
    }
    if feed_info is not None:
        files["feed_info.txt"] = f"feed_publisher_name,feed_start_date,feed_end_date\n{feed_info}\n"
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return buffer.getvalue()
