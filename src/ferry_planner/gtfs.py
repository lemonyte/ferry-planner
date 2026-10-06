from __future__ import annotations

import csv
import io
import math
import zipfile
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping
    from datetime import tzinfo

MAX_STOP_DISTANCE_KM = 2
"""Stops further than this from every location are ignored."""
KM_PER_DEGREE = 111.2
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
DATE_FORMAT = "%Y%m%d"
SERVICE_ADDED = "1"
SECONDS_PER_DAY = 24 * 60 * 60


class GtfsSailing(NamedTuple):
    departure: datetime
    arrival: datetime


class GtfsFeed:
    """Sailings from a GTFS feed archive, looked up by the IDs of the locations nearest to the feed's stops."""

    def __init__(self, data: bytes, /, *, locations: Mapping[str, tuple[float, float]], timezone: tzinfo) -> None:
        """Parse a GTFS feed.

        `locations` maps location IDs to `(latitude, longitude)` coordinates.
        """
        self._timezone = timezone
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            stop_locations = {
                row["stop_id"]: _nearest_location(float(row["stop_lat"]), float(row["stop_lon"]), locations)
                for row in _read_table(archive, "stops.txt")
            }
            # Date range that the feed has schedules for, if it says so.
            self._start_date: date | None = None
            self._end_date: date | None = None
            if "feed_info.txt" in archive.namelist():
                feed_info = next(_read_table(archive, "feed_info.txt"), {})
                if feed_info.get("feed_start_date"):
                    self._start_date = _parse_date(feed_info["feed_start_date"])
                if feed_info.get("feed_end_date"):
                    self._end_date = _parse_date(feed_info["feed_end_date"])
            trip_services = {row["trip_id"]: row["service_id"] for row in _read_table(archive, "trips.txt")}
            # Weekdays and date range that each service runs on.
            self._calendar = {
                row["service_id"]: (
                    tuple(row[weekday] == "1" for weekday in WEEKDAYS),
                    _parse_date(row["start_date"]),
                    _parse_date(row["end_date"]),
                )
                for row in _read_table(archive, "calendar.txt")
            }
            # Dates that a service is added to or removed from, regardless of its calendar.
            self._calendar_dates = {
                (row["service_id"], _parse_date(row["date"])): row["exception_type"] == SERVICE_ADDED
                for row in _read_table(archive, "calendar_dates.txt")
            }
            trip_stops: dict[str, list[tuple[int, str | None, int, int]]] = {}
            for row in _read_table(archive, "stop_times.txt"):
                trip_stops.setdefault(row["trip_id"], []).append(
                    (
                        int(row["stop_sequence"]),
                        stop_locations.get(row["stop_id"]),
                        _parse_seconds(row["arrival_time"]),
                        _parse_seconds(row["departure_time"]),
                    ),
                )
        # Services, departure and arrival times in seconds since the start of the service day,
        # for each pair of locations.
        self._sailings: dict[tuple[str, str], list[tuple[tuple[str, str], int, int]]] = {}
        for trip_id, stops in trip_stops.items():
            stops.sort()
            for index, (_, origin, _, departure) in enumerate(stops):
                for _, destination, arrival, _ in stops[index + 1 :]:
                    if origin and destination:
                        # The BC Ferries feed lists the dates that a single trip is added to or removed from
                        # under a service named after both the trip's service and the trip,
                        # which takes priority over the trip's service.
                        service_id = trip_services[trip_id]
                        self._sailings.setdefault((origin, destination), []).append(
                            ((service_id + trip_id, service_id), departure, arrival),
                        )

    def covers(self, date: date, /) -> bool:
        """Check if the feed has schedules for a date."""
        return (self._start_date is None or self._start_date <= date) and (
            self._end_date is None or date <= self._end_date
        )

    def sailings(self, origin_id: str, destination_id: str, date: date, /) -> list[GtfsSailing]:
        """Get the sailings departing from a location on a date."""
        sailings = set()
        # Sailings that depart past midnight are listed under the day before, which is their service day.
        for days_before in (0, 1):
            service_date = date - timedelta(days=days_before)
            midnight = datetime.combine(service_date, time(), tzinfo=self._timezone)
            for service_ids, departure, arrival in self._sailings.get((origin_id, destination_id), ()):
                if departure // SECONDS_PER_DAY == days_before and self._runs_on(service_ids, service_date):
                    sailings.add(
                        GtfsSailing(
                            departure=midnight + timedelta(seconds=departure),
                            arrival=midnight + timedelta(seconds=arrival),
                        ),
                    )
        return sorted(sailings)

    def _runs_on(self, service_ids: tuple[str, ...], date: date, /) -> bool:
        """Check if the first of the services that says anything about a date runs on it."""
        for service_id in service_ids:
            exception = self._calendar_dates.get((service_id, date))
            if exception is not None:
                return exception
        for service_id in service_ids:
            if service_id in self._calendar:
                weekdays, start_date, end_date = self._calendar[service_id]
                return weekdays[date.weekday()] and start_date <= date <= end_date
        return False


def _read_table(archive: zipfile.ZipFile, name: str, /) -> Iterator[dict[str, str]]:
    with archive.open(name) as file:
        yield from csv.DictReader(io.TextIOWrapper(file, encoding="utf-8-sig"))


def _parse_date(value: str, /) -> date:
    return datetime.strptime(value, DATE_FORMAT).date()  # noqa: DTZ007 Only the date is used.


def _parse_seconds(value: str, /) -> int:
    """Parse a `HH:MM:SS` time, which can be past 24:00:00 for trips that run over midnight."""
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def _nearest_location(
    latitude: float,
    longitude: float,
    locations: Mapping[str, tuple[float, float]],
    /,
) -> str | None:
    def distance(location_id: str) -> float:
        location_latitude, location_longitude = locations[location_id]
        return math.hypot(
            latitude - location_latitude,
            (longitude - location_longitude) * math.cos(math.radians(latitude)),
        )

    nearest = min(locations, key=distance, default=None)
    if nearest is None or distance(nearest) * KM_PER_DEGREE > MAX_STOP_DISTANCE_KM:
        return None
    return nearest
