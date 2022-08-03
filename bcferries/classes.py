import hashlib
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Union
from urllib.parse import quote

from pydantic import BaseModel, validator

ConnectionId = str
LocationId = str
Route = list[str]


class ConnectionsCache:
    def __init__(self):
        self.connections = {}
        self.city_connections = {}


# enum classes
class ConnectionType(Enum):
    NONE = 'NONE'
    FERRY = 'FERRY'
    CAR = 'CAR'
    BUS = 'BUS'
    AIR = 'AIR'


class LocationType(Enum):
    TERMINAL = 'TERMINAL'
    CITY = 'CITY'


class TimeIntervalType(Enum):
    FREE = 'FREE'  # extra time before segments
    WAIT = 'WAIT'  # wait at terminal
    TRAVEL = 'TRAVEL'  # travel by car/ferry/etc (see ConnectionType)


# data model classes
class FerrySailing(BaseModel):
    depart_time: str
    arrive_time: str
    duration: str
    # price: float


class FerrySchedule(BaseModel):
    date: str
    origin: str
    destination: str
    sailings: list[FerrySailing]
    url: str


class Location(BaseModel):
    id: LocationId
    name: str
    type: LocationType
    land_group: Optional[str] = None

    def map_parameter(self) -> str:
        raise NotImplementedError


class Terminal(Location):
    long_id: str
    info_url: str
    address: str
    coordinates: str  # string '{latitude:float},{longitude:float}'
    type: Literal[LocationType.TERMINAL] = LocationType.TERMINAL
    veh_close: Optional[int] = None  # vehicles check-in close time in minutes
    foot_close: Optional[int] = None  # foot passangers check-in close time in minutes
    res_open: Optional[int] = None  # booking check-in open time in minutes
    res_close: Optional[int] = None  # booking check-in close time in minutes
    res_peak_extra: Optional[int] = None  # booking check-in extra time required at peak season
    assured_open: Optional[int] = None  # assured loading check-in open time in minutes
    assured_close: Optional[int] = None  # assured loading check-in close time in minutes
    hostled_open: Optional[int] = None  # hostled vehicles check-in open time in minutes
    hostled_close: Optional[int] = None  # hostled vehicles check-in close time in minutes

    # add Terminal text to name to avoid confusion with cities
    @validator('name')
    def _validate_name(cls, value: str):
        if 'terminal' in value.lower():
            return value
        elif value.endswith(')'):
            return value[:-1] + " Terminal)"
        else:
            return value + " (Terminal)"

    def map_parameter(self) -> str:
        return self.coordinates


class City(Location):
    region: str
    province: str
    country: str
    type: Literal[LocationType.CITY] = LocationType.CITY

    def map_parameter(self) -> str:
        return ','.join([self.name, self.province, self.country])


class Connection(BaseModel):
    id: ConnectionId
    origin: Union[Terminal, City] = None  # temp
    destination: Union[Terminal, City] = None  # temp
    duration: int = None  # temp
    distance: float
    fuel: float
    type: ConnectionType


class FerryConnection(Connection):
    origin: Terminal = None  # temp
    destination: Terminal = None  # temp
    duration: int = None  # temp
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

    def __str__(self):
        return f"{self.start.strftime('%H:%M')} {self.description}"


class RoutesOptions(BaseModel):
    origin: str
    destination: str

    @validator('destination')
    def _validate_route(cls, value: str, values: dict) -> str:
        if 'origin' in values.keys() and value == values['origin']:
            raise ValueError('origin and destination cannot be the same')
        return value


class ScheduleOptions(RoutesOptions):
    date: datetime

    @validator('date', pre=True)
    def _parse_date(cls, value: Union[str, datetime]) -> datetime:
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d')
        return value


class RoutePlansOptions(ScheduleOptions):
    show_all: bool = False
    assured: bool = False
    reservation: bool = False
    hostled: bool = False
    buffer: int = 15

    @validator('date')
    def _validate_date(cls, value: Optional[datetime]) -> datetime:
        if not value:
            value = datetime.now()
        if value.date() < datetime.now().date():
            raise ValueError("date cannot be in the past")
        return value


class RoutePlanSegment(BaseModel):
    connection: Union[FerryConnection, CarConnection, AirConnection, BusConnection]  # FIXME
    times: list[TimeInterval] = []
    schedule_url: Optional[str] = None


class RoutePlan(BaseModel):
    segments: list[RoutePlanSegment] = None  # temp
    hash: str = None  # temp
    duration: int = None  # temp
    depart_time: datetime = None  # temp
    arrive_time: datetime = None  # temp
    driving_duration: int = 0
    driving_distance: float = 0
    map_url: Optional[str] = None

    def init(self, _segments: list[RoutePlanSegment]):
        # if not values.get('segments'):  # FIXME: hack
        #     values['segments'] = []
        #     return values
        segments: list[RoutePlanSegment] = []
        for segment in _segments:
            segments.append(
                RoutePlanSegment(
                    connection=segment.connection,
                    times=deepcopy(segment.times),
                    schedule_url=segment.schedule_url,
                )
            )
        if len(segments) == 0:
            return  # can we be here?

        # if first segment is driving, we can shift it to second segment
        # in order to arrive just in time for ferry
        first_segment = segments[0]
        if first_segment.connection.type == ConnectionType.CAR and len(segments) > 1:
            free_time = segments[1].times[0].start - first_segment.times[-1].end
            for t in first_segment.times:
                t.start += free_time
                t.end += free_time

        # add free time to segments
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
                    )
                )

        # add departure
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

        # add arrival
        last_segment = segments[-1]
        arrive_time = last_segment.times[-1].end
        self.arrive_time = arrive_time
        last_segment.times.append(
            TimeInterval(
                type=TimeIntervalType.TRAVEL,
                start=arrive_time,
                end=arrive_time,
                description=f"Arrive at {last_segment.connection.destination.name}",
            )
        )

        self.duration = int((arrive_time - depart_time).total_seconds())
        driving_distance = 0.0
        hash = hashlib.md5()
        # calculate distance and hash
        for s in segments:
            driving_distance += s.connection.distance
            hash.update(s.connection.destination.id.encode('utf-8'))
            for t in s.times:
                hash.update(t.start.isoformat().encode('utf-8'))
                if t.type == TimeIntervalType.TRAVEL and s.connection.type == ConnectionType.CAR:
                    self.driving_duration += int((t.end - t.start).total_seconds())
        self.driving_distance = driving_distance
        self.segments = segments
        self.hash = hash.hexdigest()

        # make google maps url
        url = 'https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}'
        waypoints = []
        for s in segments[1:]:
            waypoints.append(s.connection.origin.map_parameter())
        self.map_url = url.format(
            origin=quote(first_segment.connection.origin.map_parameter()),
            destination=quote(last_segment.connection.destination.map_parameter()),
            waypoints=quote('|'.join(waypoints)),
        )
