from __future__ import annotations

import csv
import io
import logging
import math
import zipfile
from collections import deque
from datetime import date, datetime, time, timedelta
from itertools import pairwise
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping
    from datetime import tzinfo

MAX_STOP_DISTANCE_KM = 0.5
"""Stops further than this from every location are ignored.

Less than half the distance between the two terminals closest to each other, so no stop is near two of them.
"""
MAX_TRANSFER_SECONDS = 2 * 60 * 60
"""Longest wait between two trips of a sailing."""
KM_PER_DEGREE = 111.2
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
DATE_FORMAT = "%Y%m%d"
SERVICE_ADDED = "1"
NOT_AVAILABLE = "1"
SECONDS_PER_DAY = 24 * 60 * 60


class GtfsSailing(NamedTuple):
    departure: datetime
    arrival: datetime
    stops: tuple[str, ...] = ()
    """IDs of the locations that the sailing calls at on the way."""


class _Call(NamedTuple):
    """Stop of a trip at a location.

    Times are in seconds since the start of the service day.
    """

    sequence: int
    location: str
    arrival: int
    departure: int
    can_board: bool
    can_alight: bool


class _Leg(NamedTuple):
    """Part of a trip between two locations that it calls at one after the other.

    Times are in seconds since the start of the service day.
    """

    departure: int
    arrival: int
    origin: str
    destination: str
    trip_id: str
    can_board: bool
    can_alight: bool


class GtfsFeed:
    """Sailings from a GTFS feed archive, looked up by the IDs of the locations nearest to the feed's stops."""

    def __init__(self, data: bytes, /, *, locations: Mapping[str, tuple[float, float]], timezone: tzinfo) -> None:
        """Parse a GTFS feed.

        `locations` maps location IDs to `(latitude, longitude)` coordinates.
        """
        self._timezone = timezone
        # Sailings that have been looked up, as the route planner asks for the same ones many times over.
        self._sailings: dict[tuple[str, str, date], list[GtfsSailing]] = {}
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            stop_locations = {
                row["stop_id"]: _nearest_location(float(row["stop_lat"]), float(row["stop_lon"]), locations)
                for row in _read_table(archive, "stops.txt")
                # Stops that are not boarded at, such as entrances, can have no coordinates.
                if row.get("stop_lat") and row.get("stop_lon")
            }
            # Date range that the feed has schedules for, if it says so.
            self._start_date: date | None = None
            self._end_date: date | None = None
            feed_info = next(_read_table(archive, "feed_info.txt", optional=True), {})
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
                for row in _read_table(archive, "calendar.txt", optional=True)
            }
            # Dates that a service is added to or removed from, regardless of its calendar.
            self._calendar_dates = {
                (row["service_id"], _parse_date(row["date"])): row["exception_type"] == SERVICE_ADDED
                for row in _read_table(archive, "calendar_dates.txt", optional=True)
            }
            self._transfer_seconds = _read_transfer_seconds(archive, stop_locations)
            trip_calls: dict[str, list[_Call]] = {}
            for row in _read_table(archive, "stop_times.txt"):
                location = stop_locations.get(row["stop_id"])
                # Either time stands in for the other, and stops that are only passed can have neither.
                arrival = row["arrival_time"] or row["departure_time"]
                departure = row["departure_time"] or row["arrival_time"]
                if location and arrival and departure:
                    trip_calls.setdefault(row["trip_id"], []).append(
                        _Call(
                            sequence=int(row["stop_sequence"]),
                            location=location,
                            arrival=_parse_seconds(arrival),
                            departure=_parse_seconds(departure),
                            can_board=row.get("pickup_type") != NOT_AVAILABLE,
                            can_alight=row.get("drop_off_type") != NOT_AVAILABLE,
                        ),
                    )
        # Services and legs of each trip.
        self._legs: list[tuple[tuple[str, str], _Leg]] = []
        for trip_id, calls in trip_calls.items():
            # The BC Ferries feed lists the dates that a single trip is added to or removed from
            # under a service named after both the trip's service and the trip,
            # which takes priority over the trip's service.
            service_id = trip_services[trip_id]
            for call, next_call in pairwise(sorted(calls)):
                if call.location != next_call.location:
                    self._legs.append(
                        (
                            (service_id + trip_id, service_id),
                            _Leg(
                                departure=call.departure,
                                arrival=next_call.arrival,
                                origin=call.location,
                                destination=next_call.location,
                                trip_id=trip_id,
                                can_board=call.can_board,
                                can_alight=next_call.can_alight,
                            ),
                        ),
                    )
        served = {location for _, leg in self._legs for location in (leg.origin, leg.destination)}
        if not served.issuperset(locations):
            logging.getLogger(self.__class__.__name__).warning(
                "no sailings in the GTFS feed for %s",
                ", ".join(sorted(set(locations) - served)),
            )

    def covers(self, date: date, /) -> bool:
        """Check if the feed has schedules for a date."""
        return (self._start_date is None or self._start_date <= date) and (
            self._end_date is None or date <= self._end_date
        )

    def sailings(self, origin_id: str, destination_id: str, date: date, /) -> list[GtfsSailing]:
        """Get the sailings departing from a location on a date."""
        key = (origin_id, destination_id, date)
        if key not in self._sailings:
            self._sailings[key] = self._find_sailings(origin_id, destination_id, date)
        return list(self._sailings[key])

    def _find_sailings(self, origin_id: str, destination_id: str, date: date, /) -> list[GtfsSailing]:
        sailings = set()
        # Sailings that depart past midnight are listed under the day before, which is their service day.
        for days_before in (0, 1):
            service_date = date - timedelta(days=days_before)
            midnight = datetime.combine(service_date, time(), tzinfo=self._timezone)
            legs = [leg for service_ids, leg in self._legs if self._runs_on(service_ids, service_date)]
            for departure, arrival, stops in _find_journeys(legs, origin_id, destination_id, self._transfer_seconds):
                if departure // SECONDS_PER_DAY == days_before:
                    sailings.add(
                        GtfsSailing(
                            departure=midnight + timedelta(seconds=departure),
                            arrival=midnight + timedelta(seconds=arrival),
                            stops=stops,
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


def _read_table(archive: zipfile.ZipFile, name: str, /, *, optional: bool = False) -> Iterator[dict[str, str]]:
    if optional and name not in archive.namelist():
        return
    with archive.open(name) as file:
        yield from csv.DictReader(io.TextIOWrapper(file, encoding="utf-8-sig"))


def _read_transfer_seconds(archive: zipfile.ZipFile, stop_locations: Mapping[str, str | None], /) -> dict[str, int]:
    """Get the shortest time to change trips in at each location that has one."""
    transfer_seconds: dict[str, int] = {}
    for row in _read_table(archive, "transfers.txt", optional=True):
        location = stop_locations.get(row["from_stop_id"])
        if location and location == stop_locations.get(row["to_stop_id"]) and row.get("min_transfer_time"):
            transfer_seconds[location] = max(transfer_seconds.get(location, 0), int(row["min_transfer_time"]))
    return transfer_seconds


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


def _find_journeys(
    legs: Iterable[_Leg],
    origin: str,
    destination: str,
    transfer_seconds: Mapping[str, int],
    /,
) -> list[tuple[int, int, tuple[str, ...]]]:
    """Find the departure, arrival, and stops on the way of the sailings between two locations on a service day.

    The BC Ferries feed lists each part of a sailing that calls at several terminals as a trip of its own,
    the same as a sailing that connects with another, so a sailing can be made of several trips.
    """
    legs_from: dict[str, list[_Leg]] = {}
    for leg in legs:
        legs_from.setdefault(leg.origin, []).append(leg)
    # Number of transfers and stops on the way for each departure and arrival.
    sailings: dict[tuple[int, int], tuple[int, tuple[str, ...]]] = {}
    for first_leg in legs_from.get(origin, ()):
        path = _fastest_path(first_leg, destination, legs_from, transfer_seconds)
        if path:
            times = (first_leg.departure, path[-1].arrival)
            sailing = (
                sum(leg.trip_id != next_leg.trip_id for leg, next_leg in pairwise(path)),
                tuple(leg.destination for leg in path[:-1]),
            )
            sailings[times] = min(sailing, sailings.get(times, sailing))
    return [
        (departure, arrival, stops)
        for (departure, arrival), (transfers, stops) in sailings.items()
        # Changing trips is only worth it when no later sailing arrives as early.
        if not transfers
        or not any(
            other_departure >= departure
            and other_arrival <= arrival
            and (other_departure, other_arrival) != (departure, arrival)
            for other_departure, other_arrival in sailings
        )
    ]


def _fastest_path(
    first_leg: _Leg,
    destination: str,
    legs_from: Mapping[str, list[_Leg]],
    transfer_seconds: Mapping[str, int],
    /,
) -> list[_Leg]:
    """Find the legs that arrive at a destination the earliest after a first leg, with as few legs as possible."""
    if not first_leg.can_board:
        return []
    previous_legs: dict[_Leg, _Leg | None] = {first_leg: None}
    last_leg = None
    queue = deque((first_leg,))
    while queue:
        leg = queue.popleft()
        if leg.destination == destination:
            if leg.can_alight and (last_leg is None or leg.arrival < last_leg.arrival):
                last_leg = leg
        # Returning to the origin only makes for a slower version of a later sailing.
        elif leg.destination != first_leg.origin:
            for next_leg in legs_from.get(leg.destination, ()):
                wait = next_leg.departure - leg.arrival
                if next_leg.trip_id == leg.trip_id:
                    can_continue = wait >= 0
                else:
                    can_continue = (
                        leg.can_alight
                        and next_leg.can_board
                        and transfer_seconds.get(leg.destination, 0) <= wait <= MAX_TRANSFER_SECONDS
                    )
                if can_continue and next_leg not in previous_legs:
                    previous_legs[next_leg] = leg
                    queue.append(next_leg)
    path = []
    while last_leg:
        path.append(last_leg)
        last_leg = previous_legs[last_leg]
    return path[::-1]
