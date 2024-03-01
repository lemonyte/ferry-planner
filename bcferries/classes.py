from __future__ import annotations

import hashlib
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Literal
from urllib.parse import quote

from pydantic import BaseModel, validator
from zoneinfo import ZoneInfo

ConnectionId = str
LocationId = str
Route = list[str]


class ConnectionsCache:
    def __init__(self) -> None:
        self.connections = {}
        self.city_connections = {}


# enum classes
class ConnectionType(Enum):
    NONE = "NONE"
    FERRY = "FERRY"
    CAR = "CAR"
    BUS = "BUS"
    AIR = "AIR"


class LocationType(Enum):
    TERMINAL = "TERMINAL"
    CITY = "CITY"


class TimeIntervalType(Enum):
    FREE = "FREE"  # Extra time between segments.
    WAIT = "WAIT"  # Wait at terminal.
    TRAVEL = "TRAVEL"  # Travel by car/ferry/etc (see ConnectionType).


class FerrySailing(BaseModel):
    depart_time: str
    arrive_time: str
    duration: str
    # TODO: price: float


class FerrySchedule(BaseModel):
    date: datetime
    origin: str
    destination: str
    sailings: list[FerrySailing]
    url: str


class Location(BaseModel):
    id: LocationId
    name: str
    type: LocationType
    land_group: str | None = None

    def map_parameter(self) -> str:
        raise NotImplementedError


class Terminal(Location):
    long_id: str
    info_url: str
    address: str
    coordinates: str  # String format "{latitude:float},{longitude:float}".
    type: Literal[LocationType.TERMINAL] = LocationType.TERMINAL
    veh_close: int | None = None  # Vehicles check-in close time in minutes.
    foot_close: int | None = None  # Foot passangers check-in close time in minutes.
    res_open: int | None = None  # Booking check-in open time in minutes.
    res_close: int | None = None  # Booking check-in close time in minutes.
    res_peak_extra: int | None = None  # Booking check-in extra time required at peak season.
    assured_open: int | None = None  # Assured loading check-in open time in minutes.
    assured_close: int | None = None  # Assured loading check-in close time in minutes.
    hostled_open: int | None = None  # Hostled vehicles check-in open time in minutes.
    hostled_close: int | None = None  # Hostled vehicles check-in close time in minutes.

    # Add "terminal" text to name to avoid confusion with cities.
    @validator("name")
    def _validate_name(cls, value: str) -> str:  # noqa: N805
        if "terminal" in value.lower():
            return value
        if value.endswith(")"):
            return value[:-1] + " Terminal)"
        return value + " (Terminal)"

    def map_parameter(self) -> str:
        return self.coordinates


class City(Location):
    region: str
    province: str
    country: str
    type: Literal[LocationType.CITY] = LocationType.CITY

    def map_parameter(self) -> str:
        return f"{self.name},{self.province},{self.country}"


class Connection(BaseModel):
    id: ConnectionId
    origin: Location = None  # type: ignore[None]
    destination: Location = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    distance: float
    fuel: float
    type: ConnectionType


class FerryConnection(Connection):
    origin: Terminal = None  # type: ignore[None]
    destination: Terminal = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    distance: float = 0.2
    fuel: float = 0.2
    type: Literal[ConnectionType.FERRY] = ConnectionType.FERRY
    bookable: bool = False


class CarConnection(Connection):
    type: Literal[ConnectionType.CAR] = ConnectionType.CAR


class AirConnection(Connection):
    type: Literal[ConnectionType.AIR] = ConnectionType.AIR


class BusConnection(Connection):
    type: Literal[ConnectionType.BUS] = ConnectionType.BUS


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

    @validator("destination")
    def _validate_route(cls, value: str, values: dict) -> str:  # noqa: N805
        if "origin" in values and value == values["origin"]:
            msg = "origin and destination cannot be the same"
            raise ValueError(msg)
        return value


class ScheduleOptions(RoutesOptions):
    date: datetime

    @validator("date", pre=True)
    def _parse_date(cls, value: str | datetime) -> datetime:  # noqa: N805
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d")  # noqa: DTZ007
        return value


class RoutePlansOptions(ScheduleOptions):
    show_all: bool = False
    assured: bool = False
    reservation: bool = False
    hostled: bool = False
    buffer: int = 15

    @validator("date")
    def _validate_date(cls, value: datetime | None) -> datetime:  # noqa: N805
        if not value:
            value = datetime.now()  # noqa: DTZ005
        # if value.date() < datetime.now().date():
        #     raise ValueError("date cannot be in the past")
        return value


class RoutePlanSegment(BaseModel):
    connection: FerryConnection | CarConnection | AirConnection | BusConnection  # TODO: FIXME
    times: list[TimeInterval] = []
    schedule_url: str | None = None


class RoutePlan(BaseModel):
    segments: list[RoutePlanSegment] = None  # type: ignore[None]
    hash: str = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    depart_time: datetime = None  # type: ignore[None]
    arrive_time: datetime = None  # type: ignore[None]
    driving_duration: int = 0
    driving_distance: float = 0
    map_url: str | None = None

    def init(self, _segments: list[RoutePlanSegment]) -> None:
        segments: list[RoutePlanSegment] = [
            RoutePlanSegment(
                connection=segment.connection,
                times=deepcopy(segment.times),
                schedule_url=segment.schedule_url,
            )
            for segment in _segments
        ]
        if len(segments) == 0:
            return  # can we be here?

        # If first segment is driving, we can shift it to second segment
        # in order to arrive just in time for ferry.
        first_segment = segments[0]
        if first_segment.connection.type == ConnectionType.CAR and len(segments) > 1:
            free_time = segments[1].times[0].start - first_segment.times[-1].end
            for time in first_segment.times:
                time.start += free_time
                time.end += free_time

        # If the only segment is car travel, make sure start time is in Vancouver time zone
        if first_segment.connection.type == ConnectionType.CAR and len(segments) == 1:
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
        self.depart_time = depart_time
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
        self.arrive_time = arrive_time
        last_segment.times.append(
            TimeInterval(
                type=TimeIntervalType.TRAVEL,
                start=arrive_time,
                end=arrive_time,
                description=f"Arrive at {last_segment.connection.destination.name}",
            ),
        )

        self.duration = int((arrive_time - depart_time).total_seconds())

        # Calculate distance and hash.
        driving_distance = 0.0
        hash = hashlib.md5()  # noqa: S324
        for segment in segments:
            driving_distance += segment.connection.distance
            hash.update(segment.connection.destination.id.encode("utf-8"))
            for time in segment.times:
                hash.update(time.start.isoformat().encode("utf-8"))
                if time.type == TimeIntervalType.TRAVEL and segment.connection.type == ConnectionType.CAR:
                    self.driving_duration += int((time.end - time.start).total_seconds())
        self.driving_distance = driving_distance
        self.segments = segments
        self.hash = hash.hexdigest()

        # Create Google Maps URL.
        url = "https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}"
        waypoints = [segment.connection.origin.map_parameter() for segment in segments[1:]]
        self.map_url = url.format(
            origin=quote(first_segment.connection.origin.map_parameter()),
            destination=quote(last_segment.connection.destination.map_parameter()),
            waypoints=quote("|".join(waypoints)),
        )
