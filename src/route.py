# ruff: noqa: DTZ007
from __future__ import annotations

import hashlib
from collections.abc import MutableSequence, Sequence
from copy import deepcopy
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING
from urllib.parse import quote
from zoneinfo import ZoneInfo

from pydantic import BaseModel

from .connection import CarConnection, Connection, ConnectionId, FerryConnection
from .data import connections, location_connections

if TYPE_CHECKING:
    from .location import LocationId
    from .options import RoutePlansOptions
    from .schedule import ScheduleGetter

Route = Sequence[str]


class TimeIntervalType(Enum):
    FREE = "FREE"
    """Extra time between segments."""
    WAIT = "WAIT"
    """Wait at terminal."""
    TRAVEL = "TRAVEL"
    """Travel by car/ferry/etc (see ConnectionType)."""


class TimeInterval(BaseModel):
    start: datetime
    end: datetime
    description: str
    type: TimeIntervalType

    def __str__(self) -> str:
        return f"{self.start.strftime('%H:%M')} {self.description}"


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


def find_routes(origin_id: str, destination_id: str) -> list[Route]:
    routes = []
    find_routes_recurse(origin_id, destination_id, routes)
    return routes


def find_routes_recurse(  # noqa: C901, PLR0912, PLR0913
    next_point: str,
    end_point: str,
    routes: list[Route],
    current_route: list[LocationId] | None = None,
    dead_ends: list[ConnectionId] | None = None,
    lands: list[str] | None = None,
    last_connection_type: type[Connection] = Connection,
) -> bool:
    if current_route is None:
        current_route = []
    if dead_ends is None:
        dead_ends = []
    if lands is None:
        lands = []
    current_route.append(next_point)
    if next_point == end_point:
        routes.append(current_route.copy())
        del current_route[-1]
        return True
    connections_cache = location_connections[next_point]
    if end_point in connections_cache.city_connections:
        current_route.append(end_point)
        routes.append(current_route.copy())
        del current_route[-2:]
        return True
    res = False
    for connection in connections_cache.connections.values():
        if connection.destination.id in current_route or connection.id in dead_ends:
            continue
        if isinstance(connection, CarConnection) and last_connection_type is CarConnection:
            continue  # Drive only shortest way between terminals.
        if (
            isinstance(connection, FerryConnection)
            and connection.destination.land_group
            and connection.destination.land_group in lands
        ):
            continue
        if isinstance(connection, FerryConnection) and connection.origin.land_group:
            lands.append(connection.origin.land_group)
        else:
            lands.append("")
        if find_routes_recurse(
            connection.destination.id,
            end_point,
            routes,
            current_route,
            dead_ends,
            lands,
            type(connection),
        ):
            res = True
        else:
            dead_ends.append(connection.id)
        del lands[-1]
    del current_route[-1]
    return res


def make_route_plans(
    routes: list[Route],
    options: RoutePlansOptions,
    schedule_source: ScheduleGetter,
) -> list[RoutePlan]:
    all_plans = []
    for route in routes:
        route_plans = []
        segments = []
        add_plan_segment(
            route,
            1,
            segments,
            options.date,
            route_plans,
            options,
            schedule_source,
        )
        all_plans.extend(route_plans)
    return all_plans


def add_plan_segment(  # noqa: PLR0913
    route: Route,
    destination_index: int,
    segments: list[RoutePlanSegment],
    start_time: datetime,
    plans: list[RoutePlan],
    options: RoutePlansOptions,
    schedule_source: ScheduleGetter,
) -> bool:
    res = False
    try:
        if destination_index == len(route):
            if not segments:  # empty list?
                return False  # can we be here?
            plan = RoutePlan.from_segments(segments)
            plans.append(plan)
            return True
        id_from = route[destination_index - 1]
        id_to = route[destination_index]
        connection_id = f"{id_from}-{id_to}"
        connection = connections[connection_id]
        if isinstance(connection, FerryConnection):
            res = add_ferry_connection(
                route,
                destination_index,
                segments,
                start_time,
                plans,
                options,
                id_from,
                id_to,
                connection,
                schedule_source,
            )
        if isinstance(connection, CarConnection):
            if not options.show_all and connection.duration > 6 * 60 * 60:
                return False
            arrive_time = start_time + timedelta(seconds=connection.duration)
            if not options.show_all and start_time.date() != arrive_time.date():
                return False  # overnight
            segment = RoutePlanSegment(connection=connection)
            segment.times.append(
                TimeInterval(
                    type=TimeIntervalType.TRAVEL,
                    start=start_time,
                    end=arrive_time,
                    description=f"Drive {round(connection.distance)} km to {connection.destination.name}",
                ),
            )
            segments.append(segment)
            res = add_plan_segment(
                route,
                destination_index + 1,
                segments,
                arrive_time,
                plans,
                options,
                schedule_source,
            )
    finally:
        delete_start = destination_index - 1
        del segments[delete_start:]
    return res


def add_ferry_connection(  # noqa: C901, PLR0912, PLR0913
    route: Route,
    destination_index: int,
    segments: list[RoutePlanSegment],
    start_time: datetime,
    plans: list[RoutePlan],
    options: RoutePlansOptions,
    id_from: str,
    id_to: str,
    connection: FerryConnection,
    schedule_source: ScheduleGetter,
) -> bool:
    res = False
    depature_terminal = connection.origin
    day = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    schedule = schedule_source(id_from, id_to, day)
    if not schedule:
        return False
    for sailing in schedule.sailings:
        depart_time = day + datetime_to_timedelta(datetime.strptime(sailing.depart_time, "%H:%M:%S"))
        arrive_time = day + datetime_to_timedelta(datetime.strptime(sailing.arrive_time, "%H:%M:%S"))
        if arrive_time < depart_time:
            arrive_time += timedelta(days=1)
        if not options.show_all and start_time.date() != arrive_time.date():
            break  # Skip routes that take more than one day.
        if depart_time < start_time:
            continue
        deadline_name = "departure"
        wait_minutes = 0
        if options.hostled and depature_terminal.hostled_close and depature_terminal.hostled_close > 0:
            deadline_name = "hostled vehicles checkin close"
            wait_minutes = depature_terminal.hostled_close
        if options.assured and depature_terminal.assured_close and depature_terminal.assured_close > 0:
            deadline_name = "assured loading checkin close"
            wait_minutes = depature_terminal.assured_close
        elif depature_terminal.res_close and depature_terminal.res_close > 0 and connection.bookable:
            deadline_name = "booking checkin close"
            wait_minutes = depature_terminal.res_close
        elif depature_terminal.veh_close and depature_terminal.veh_close > 0:
            deadline_name = "vehicles checkin close"
            wait_minutes = depature_terminal.veh_close
        elif depature_terminal.foot_close and depature_terminal.foot_close > 0:
            deadline_name = "foot passengers checkin close"
            wait_minutes = depature_terminal.foot_close
        deadline_time = depart_time - timedelta(minutes=wait_minutes) - timedelta(minutes=options.buffer)
        if deadline_time < start_time:
            continue
        segment = RoutePlanSegment(connection=connection)
        segment.schedule_url = schedule.url
        if deadline_time < depart_time:
            description = f"Arrive at {connection.origin.name} "
            if options.buffer > 0:
                description += f"{options.buffer} minutes "
            description += f"before {deadline_name}"
            segment.times.append(
                TimeInterval(
                    type=TimeIntervalType.WAIT,
                    start=deadline_time,
                    end=depart_time,
                    description=description,
                ),
            )
        segment.times.append(
            TimeInterval(
                type=TimeIntervalType.TRAVEL,
                start=depart_time,
                end=arrive_time,
                description=f"Ferry sailing from {connection.origin.name} to {connection.destination.name}",
            ),
        )
        segments.append(segment)
        if (
            add_plan_segment(
                route,
                destination_index + 1,
                segments,
                arrive_time,
                plans,
                options,
                schedule_source,
            )
            is False
        ):
            break
        delete_start = destination_index - 1
        del segments[delete_start:]
        res = True
        if not options.show_all and sum(1 for s in segments if isinstance(s.connection, FerryConnection)) > 0:
            break
    return res


def datetime_to_timedelta(value: datetime) -> timedelta:
    return timedelta(hours=value.hour, minutes=value.minute, seconds=value.second)
