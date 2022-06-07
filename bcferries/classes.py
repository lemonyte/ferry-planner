import json
from copy import deepcopy
from datetime import datetime
from dataclasses import dataclass, fields, is_dataclass, asdict, field
from enum import Enum
from urllib.parse import quote

ConnectionId = str
LocationId = str
Route = list[str]


class ConnectionType(Enum):
    NONE = 0
    FERRY = 1
    CAR = 2
    BUS = 3
    AIR = 4


class LocationType(Enum):
    TERMINAL = 1
    CITY = 2


class TimeIntervalType(Enum):
    FREE = 0  # extra time before segments
    WAIT = 1  # wait at terminal
    TRAVEL = 2  # travel by car/ferry/etc (see connection.type)


@dataclass
class BaseDataClass:
    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, dict) and is_dataclass(f.type):
                setattr(self, f.name, f.type(**value))
            elif isinstance(value, (list, tuple)) and is_dataclass(f.type.__args__[0]):
                setattr(
                    self,
                    f.name,
                    [f.type.__args__[0](**v) if isinstance(v, dict) else v for v in value],
                )

    @classmethod
    def from_dict(cls, obj):
        if isinstance(obj, dict):
            fs = cls.__dataclass_fields__
            kv = {}
            for i in obj:
                if isinstance(obj[i], dict) and isinstance(fs[i].type, BaseDataClass):
                    kv[i] = fs[i].type.from_dict(obj[i])
                else:
                    kv[i] = obj[i]
            for k in [k for k in kv.keys() if k not in fs.keys()]:
                kv.pop(k)
            return cls(**kv)
        elif isinstance(obj, (list, tuple)) and isinstance(cls.__args__[0], BaseDataClass):
            return [cls.__args__[0].from_dict(i) for i in obj]
        else:
            return obj

    def to_dict(self):
        result = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, BaseDataClass):
                value = value.to_dict()
            elif is_dataclass(value):
                value = asdict(value)
            elif isinstance(value, (list, tuple)):
                value = [
                    v.to_dict()
                    if isinstance(v, BaseDataClass)
                    else asdict(v)
                    if is_dataclass(v)
                    else v
                    for v in value
                ]
            result[f.name] = value
        return result

    def to_json(self):
        return json.dumps(self, cls=JSONEncoderEx)


@dataclass
class FerrySailing(BaseDataClass):
    depart_time: str
    arrive_time: str
    duration: str
    # price: float


@dataclass
class FerrySchedule(BaseDataClass):
    date: str
    depart_terminal: str
    arrive_terminal: str
    sailings: list[FerrySailing]


@dataclass
class Location(BaseDataClass):
    id: LocationId
    name: str
    type: LocationType
    land_group: str = None
    # connections: dict[str, Connection] = {}
    # city_connections: dict[str, Connection] = {}


@dataclass
class Terminal(Location):
    long_id: str = None
    info_url: str = None
    location: str = None  # address
    coordinates: str = None
    type: LocationType = LocationType.TERMINAL
    veh_close: int = None  # vehicles check-in close time in minutes
    foot_close: int = None  # foot passangers check-in close time in minutes
    res_open: int = None  # booking check-in open time in minutes
    res_close: int = None  # booking check-in close time in minutes
    res_peak_extra: int = None  # booking check-in extra time required at peak season
    assured_open: int = None  # assured loading check-in open time in minutes
    assured_close: int = None  # assured loading check-in close time in minutes
    hostled_open: int = None  # hostled vehicles check-in open time in minutes
    hostled_close: int = None  # hostled vehicles check-in close time in minutes

    def map_parameter(self) -> str:
        return ','.join(self.coordinates.split(',')[::-1])


@dataclass
class City(Location):
    region: str = None
    province: str = None
    country: str = None
    type: LocationType = LocationType.CITY

    def map_parameter(self) -> str:
        return ','.join([self.name, self.province, self.country])


@dataclass
class Connection(BaseDataClass):
    id: ConnectionId
    location_from: Location
    location_to: Location
    duration: int
    distance: float
    fuel: float
    type: ConnectionType
    land_group: str = None


@dataclass
class FerryConnection(Connection):
    duration: int = None
    distance: float = 0.2
    fuel: float = 0.2
    type: ConnectionType = ConnectionType.FERRY
    bookable: bool = False


@dataclass
class CarConnection(Connection):
    type: ConnectionType = ConnectionType.CAR


@dataclass
class AirConnection(Connection):
    type: ConnectionType = ConnectionType.AIR


@dataclass
class BusConnection(Connection):
    type: ConnectionType = ConnectionType.BUS


@dataclass
class TimeInterval(BaseDataClass):
    type: TimeIntervalType
    start: datetime
    end: datetime
    description: str

    def __str__(self):
        return f"{self.start.strftime('%H:%M')} {self.description}"


@dataclass
class RoutePlanOptions:
    start_time: datetime = datetime.now()  # start time to calculate plan
    buffer_time_minutes: int = 15  # extra time to arrive before deadline
    assured_load: bool = False
    hostled: bool = False
    only_closest_ferry: bool = True
    reservation: bool = True


@dataclass
class RoutePlanSegment(BaseDataClass):
    connection: Connection
    times: list[TimeInterval] = field(default_factory=list[TimeInterval])


@dataclass
class RoutePlan(BaseDataClass):
    segments: list[RoutePlanSegment] = field(default_factory=list[RoutePlanSegment])
    duration: int = 0  # time in seconds from start to end
    driving_distance: float = 0  # total driving distance
    depart_time: int = 0
    arrive_time: int = 0
    driving_time: int = 0
    map_url: str = ''

    def __init__(self, _segments: list[RoutePlanSegment]):
        new_segments: list[RoutePlanSegment] = []
        for segment in _segments:
            new_segments.append(RoutePlanSegment(segment.connection, deepcopy(segment.times)))
        segments = new_segments
        slen = len(segments)
        if slen == 0:
            return  # can we be here?
        # if first segment is driving, we can shift it to second segment in order to arrive just in time for ferry
        first_segment = segments[0]
        if first_segment.connection.type == ConnectionType.CAR and slen > 1:
            free_time = segments[1].times[0].start - first_segment.times[-1].end
            for t in first_segment.times:
                t.start += free_time
                t.end += free_time
        # add free time to segments
        for i in range(slen - 1):
            free_start = segments[i].times[-1].end
            free_end = segments[i + 1].times[0].start
            free_time = free_end - free_start
            if free_time.total_seconds() > 0:
                segments[i].times.append(
                    TimeInterval(TimeIntervalType.FREE, free_start, free_end, "Free time")
                )
        # add arrival
        depart_time = first_segment.times[0].start
        self.depart_time = depart_time
        first_segment.times.insert(
            0,
            TimeInterval(
                TimeIntervalType.TRAVEL,
                depart_time,
                depart_time,
                f"Depart from {first_segment.connection.location_from.name}",
            ),
        )
        last_segment = segments[-1]
        arrive_time = last_segment.times[-1].end
        self.arrive_time = arrive_time
        last_segment.times.append(
            TimeInterval(
                TimeIntervalType.TRAVEL,
                arrive_time,
                arrive_time,
                f"Arrive at {last_segment.connection.location_to.name}",
            )
        )
        # calculate duration and distance
        self.duration = int((arrive_time - depart_time).total_seconds())
        self.driving_distance = 0
        for s in segments:
            self.driving_distance += s.connection.distance
            for t in s.times:
                if t.type == TimeIntervalType.TRAVEL and s.connection.type == ConnectionType.CAR:
                    self.driving_time += (t.end - t.start).total_seconds()
        self.segments = segments
        url = 'https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}'
        waypoints = []
        for s in segments[1:]:
            waypoints.append(s.connection.location_from.map_parameter())
        self.map_url = url.format(
            origin=quote(first_segment.connection.location_from.map_parameter()),
            destination=quote(last_segment.connection.location_to.map_parameter()),
            waypoints=quote('|'.join(waypoints)),
        )


class JSONEncoderEx(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif is_dataclass(o):
            return asdict(o)
        elif isinstance(o, Enum):
            return o.name
        else:
            return json.JSONEncoder.default(self, o)
