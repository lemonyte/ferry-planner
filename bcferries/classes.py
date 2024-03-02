# ruff: noqa: DTZ005, DTZ007
from __future__ import annotations

import hashlib
from abc import ABC
from collections.abc import MutableSequence, Sequence
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Self
from urllib.parse import quote
from zoneinfo import ZoneInfo

from pydantic import BaseModel, field_validator, model_validator

ConnectionId = str
LocationId = str
Route = Sequence[str]


class ConnectionsCache:
    def __init__(self) -> None:
        self.connections = {}
        self.city_connections = {}


class TimeIntervalType(Enum):
    FREE = "FREE"
    """Extra time between segments."""
    WAIT = "WAIT"
    """Wait at terminal."""
    TRAVEL = "TRAVEL"
    """Travel by car/ferry/etc (see ConnectionType)."""


class FerrySailing(BaseModel):
    depart_time: str
    arrive_time: str
    duration: str
    # TODO: price: float  # noqa: FIX002


class FerrySchedule(BaseModel):
    date: datetime
    origin: str
    destination: str
    sailings: Sequence[FerrySailing]
    url: str


class Location(BaseModel, ABC):
    id: LocationId
    name: str
    land_group: str | None = None

    @property
    def map_parameter(self) -> str:
        raise NotImplementedError


class Terminal(Location):
    long_id: str
    info_url: str
    address: str
    coordinates: str
    """String format "{latitude:float},{longitude:float}"."""
    veh_close: int | None = None
    """Vehicles check-in close time in minutes."""
    foot_close: int | None = None
    """Foot passangers check-in close time in minutes."""
    res_open: int | None = None
    """Booking check-in open time in minutes."""
    res_close: int | None = None
    """Booking check-in close time in minutes."""
    res_peak_extra: int | None = None
    """Booking check-in extra time required at peak season."""
    assured_open: int | None = None
    """Assured loading check-in open time in minutes."""
    assured_close: int | None = None
    """Assured loading check-in close time in minutes."""
    hostled_open: int | None = None
    """Hostled vehicles check-in open time in minutes."""
    hostled_close: int | None = None
    """Hostled vehicles check-in close time in minutes."""

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        """Add "terminal" text to name to avoid confusion with cities."""
        if "terminal" in value.lower():
            return value
        if value.endswith(")"):
            return value[:-1] + " Terminal)"
        return value + " (Terminal)"

    @property
    def map_parameter(self) -> str:
        return self.coordinates


class City(Location):
    region: str
    province: str
    country: str

    @property
    def map_parameter(self) -> str:
        return f"{self.name},{self.province},{self.country}"


class Connection(BaseModel, ABC):
    id: ConnectionId
    origin: Location = None  # type: ignore[None]
    destination: Location = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    distance: float
    fuel: float


class FerryConnection(Connection):
    origin: Terminal = None  # type: ignore[None]
    destination: Terminal = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    distance: float = 0.2
    fuel: float = 0.2
    bookable: bool = False


class CarConnection(Connection):
    pass


class AirConnection(Connection):
    pass


class BusConnection(Connection):
    pass


class TimeInterval(BaseModel):
    start: datetime
    end: datetime
    description: str
    type: TimeIntervalType

    def __str__(self) -> str:
        return f"{self.start.strftime('%H:%M')} {self.description}"


class RoutesOptions(BaseModel):
    origin: str
    destination: str

    @model_validator(mode="after")
    def _validate_route(self) -> Self:
        if self.origin == self.destination:
            msg = "origin and destination cannot be the same"
            raise ValueError(msg)
        return self


class ScheduleOptions(RoutesOptions):
    date: datetime

    @field_validator("date", mode="before")
    @classmethod
    def _parse_date(cls, value: str | datetime | None) -> datetime:
        if not value:
            value = datetime.now()
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d")
        return value


class RoutePlansOptions(ScheduleOptions):
    show_all: bool = False
    assured: bool = False
    reservation: bool = False
    hostled: bool = False
    buffer: int = 15


class RoutePlanSegment(BaseModel):
    connection: Connection
    times: MutableSequence[TimeInterval] = []  # TODO: make it non-mutable  # noqa: FIX002
    schedule_url: str | None = None


class RoutePlan(BaseModel):
    segments: Sequence[RoutePlanSegment] = None  # type: ignore[None]
    hash: str = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    depart_time: datetime = None  # type: ignore[None]
    arrive_time: datetime = None  # type: ignore[None]
    driving_duration: int = 0
    driving_distance: float = 0
    map_url: str | None = None

    @classmethod
    def from_segments(cls, _segments: Sequence[RoutePlanSegment], /) -> RoutePlan:  # noqa: C901
        segments = [
            RoutePlanSegment(
                connection=segment.connection,
                times=deepcopy(segment.times),
                schedule_url=segment.schedule_url,
            )
            for segment in _segments
        ]
        if len(segments) == 0:
            msg = "RoutePlan must have at least one segment"
            raise ValueError(msg)  # can we be here?

        # If first segment is driving, we can shift it to second segment
        # in order to arrive just in time for ferry.
        first_segment = segments[0]
        if isinstance(first_segment.connection, CarConnection) and len(segments) > 1:
            free_time = segments[1].times[0].start - first_segment.times[-1].end
            for time in first_segment.times:
                time.start += free_time
                time.end += free_time

        # If the only segment is car travel, make sure start time is in Vancouver time zone
        if isinstance(first_segment.connection, CarConnection) and len(segments) == 1:
            tz = ZoneInfo("America/Vancouver")
            now = datetime.now().astimezone()
            local_offset = now.astimezone().utcoffset()
            bc_offset = tz.utcoffset(now)
            if local_offset and bc_offset:
                tz_diff = bc_offset - local_offset
                current_time_bc = now - first_segment.times[0].start.astimezone() + tz_diff
                for t in first_segment.times:
                    t.start += current_time_bc
                    t.end += current_time_bc

        # Add free time to segments.
        for i in range(len(segments) - 1):
            free_start = segments[i].times[-1].end
            free_end = segments[i + 1].times[0].start
            free_time = free_end - free_start
            if free_time.total_seconds() > 0:
                segments[i].times.append(
                    TimeInterval(
                        type=TimeIntervalType.FREE,
                        start=free_start,
                        end=free_end,
                        description="Free time",
                    ),
                )

        # Add departure.
        depart_time = first_segment.times[0].start
        first_segment.times.insert(
            0,
            TimeInterval(
                type=TimeIntervalType.TRAVEL,
                start=depart_time,
                end=depart_time,
                description=f"Depart from {first_segment.connection.origin.name}",
            ),
        )

        # Add arrival.
        last_segment = segments[-1]
        arrive_time = last_segment.times[-1].end
        last_segment.times.append(
            TimeInterval(
                type=TimeIntervalType.TRAVEL,
                start=arrive_time,
                end=arrive_time,
                description=f"Arrive at {last_segment.connection.destination.name}",
            ),
        )

        # Calculate distance and hash.
        driving_duration = 0
        driving_distance = 0.0
        hash = hashlib.md5(usedforsecurity=False)
        for segment in segments:
            driving_distance += segment.connection.distance
            hash.update(segment.connection.destination.id.encode("utf-8"))
            for time in segment.times:
                hash.update(time.start.isoformat().encode("utf-8"))
                if time.type == TimeIntervalType.TRAVEL and isinstance(first_segment.connection, CarConnection):
                    driving_duration += int((time.end - time.start).total_seconds())

        # Create Google Maps URL.
        url = "https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}"
        waypoints = [segment.connection.origin.map_parameter for segment in segments[1:]]
        map_url = url.format(
            origin=quote(first_segment.connection.origin.map_parameter),
            destination=quote(last_segment.connection.destination.map_parameter),
            waypoints=quote("|".join(waypoints)),
        )

        return cls(
            segments=segments,
            hash=hash.hexdigest(),
            duration=int((arrive_time - depart_time).total_seconds()),
            depart_time=depart_time,
            arrive_time=arrive_time,
            driving_duration=driving_duration,
            driving_distance=driving_distance,
            map_url=map_url,
        )
