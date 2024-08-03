# ruff: noqa: DTZ007
from __future__ import annotations

import asyncio
import hashlib
from collections.abc import Generator, Iterable, Iterator, Sequence
from copy import deepcopy
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING
from urllib.parse import quote
from zoneinfo import ZoneInfo

from pydantic import BaseModel

from ferry_planner.connection import CarConnection, Connection, FerryConnection
from ferry_planner.data import ConnectionNotFoundError
from ferry_planner.location import City, Location
from ferry_planner.utils import datetime_to_timedelta

if TYPE_CHECKING:
    from ferry_planner.data import ConnectionDB
    from ferry_planner.options import RoutePlansOptions
    from ferry_planner.schedule import ScheduleGetter

Route = Sequence[Location]


class TimeIntervalType(Enum):
    FREE = "FREE"
    """Extra time between segments."""
    WAIT = "WAIT"
    """Wait at terminal."""
    TRAVEL = "TRAVEL"
    """Travel by car/ferry/etc (see connection.ConnectionType)."""


class TimeInterval(BaseModel):
    start: datetime
    end: datetime
    description: str
    type: TimeIntervalType

    def __str__(self) -> str:
        return f"{self.start.strftime('%H:%M')} {self.description}"


class RoutePlanSegment(BaseModel):
    # Pydantic throws an error if the type hint is Connection[Location, Location]
    # and the passed type is FerryConnection (Connection[Terminal, Terminal]).
    connection: Connection
    times: tuple[TimeInterval, ...]
    schedule_url: str | None = None


class RoutePlan(BaseModel):
    segments: tuple[RoutePlanSegment, ...]
    hash: str
    duration: int
    """Total duration in seconds."""
    depart_time: datetime
    arrive_time: datetime
    driving_duration: int = 0
    """Total driving duration in seconds."""
    driving_distance: float = 0
    """Total driving distance in kilometers."""
    map_url: str | None = None
    """Google Maps URL of the route."""

    @classmethod
    def from_segments(cls, _segments: Iterable[RoutePlanSegment], /) -> RoutePlan:  # noqa: C901
        segments = tuple(
            RoutePlanSegment(
                connection=segment.connection,
                times=deepcopy(segment.times),
                schedule_url=segment.schedule_url,
            )
            for segment in _segments
        )
        segments_len = len(segments)
        if segments_len == 0:
            msg = "route plan must have at least one segment"
            raise ValueError(msg)

        # If first segment is driving, we can shift it to second segment
        # in order to arrive just in time for ferry.
        first_segment = segments[0]
        if isinstance(first_segment.connection, CarConnection) and segments_len > 1:
            free_time = segments[1].times[0].start - first_segment.times[-1].end
            for time in first_segment.times:
                time.start += free_time
                time.end += free_time

        # If the only segment is car travel, make sure start time is in Vancouver time zone.
        if isinstance(first_segment.connection, CarConnection) and segments_len == 1:
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
        for i in range(segments_len - 1):
            free_start = segments[i].times[-1].end
            free_end = segments[i + 1].times[0].start
            free_time = free_end - free_start
            if free_time.total_seconds() > 0:
                segments[i].times = (
                    *segments[i].times,
                    TimeInterval(
                        type=TimeIntervalType.FREE,
                        start=free_start,
                        end=free_end,
                        description="Free time",
                    ),
                )

        # Add departure.
        depart_time = first_segment.times[0].start
        if not isinstance(first_segment.connection, FerryConnection):
            first_segment.times = (
                TimeInterval(
                    type=TimeIntervalType.TRAVEL,
                    start=depart_time,
                    end=depart_time,
                    description=f"Depart from {first_segment.connection.origin.name}",
                ),
                *first_segment.times,
            )

        # Add arrival.
        last_segment = segments[-1]
        arrive_time = last_segment.times[-1].end
        last_segment.times = (
            *last_segment.times,
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
        plan_hash = hashlib.sha1(usedforsecurity=False)
        for segment in segments:
            if isinstance(segment.connection, CarConnection):
                driving_duration += segment.connection.duration
                driving_distance += segment.connection.distance
            plan_hash.update(segment.connection.destination.id.encode("utf-8"))
            for time in segment.times:
                plan_hash.update(time.start.isoformat().encode("utf-8"))

        # Create Google Maps URL.
        url = "https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}"
        waypoints = (segment.connection.origin.map_parameter for segment in segments[1:])
        map_url = url.format(
            origin=quote(first_segment.connection.origin.map_parameter),
            destination=quote(last_segment.connection.destination.map_parameter),
            waypoints=quote("|".join(waypoints)),
        )

        return cls(
            segments=segments,
            hash=plan_hash.hexdigest(),
            duration=int((arrive_time - depart_time).total_seconds()),
            depart_time=depart_time,
            arrive_time=arrive_time,
            driving_duration=driving_duration,
            driving_distance=driving_distance,
            map_url=map_url,
        )


class RouteBuilder:
    def __init__(self, connection_db: ConnectionDB, /) -> None:
        self._connection_db = connection_db

    def find_routes(self, *, origin: Location, destination: Location) -> Iterator[Route]:
        return self._find_routes_recurse(next_point=origin, end_point=destination)

    def _find_routes_recurse(  # noqa: C901, PLR0912, PLR0913
        self,
        *,
        next_point: Location,
        end_point: Location,
        current_route: list[Location] | None = None,
        dead_ends: set[Connection] | None = None,
        lands: list[str] | None = None,
        last_connection_type: type[Connection] = Connection,
    ) -> Generator[Route, None, bool]:
        if current_route is None:
            current_route = []
        if dead_ends is None:
            dead_ends = set()
        if lands is None:
            lands = []
        current_route.append(next_point)
        if next_point == end_point:
            yield current_route.copy()
            del current_route[-1]
            return True
        if isinstance(end_point, City):
            # Check if a connection exists between the current location and the end point.
            try:
                _ = self._connection_db.from_to_location(next_point, end_point)
            except ConnectionNotFoundError:
                pass
            else:
                current_route.append(end_point)
                yield current_route.copy()
                del current_route[-2:]
                return True
        result = False
        for connection in self._connection_db.from_location(next_point):
            if connection.destination in current_route or connection in dead_ends:
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
            recursion_result = yield from self._find_routes_recurse(
                next_point=connection.destination,
                end_point=end_point,
                current_route=current_route,
                dead_ends=dead_ends,
                lands=lands,
                last_connection_type=type(connection),
            )
            if recursion_result is True:
                result = True
            else:
                dead_ends.add(connection)
            del lands[-1]
        del current_route[-1]
        return result


class RoutePlanBuilder:
    def __init__(self, *, connection_db: ConnectionDB, schedule_getter: ScheduleGetter) -> None:
        self._connection_db = connection_db
        self._schedule_getter = schedule_getter

    async def _pre_cache_schedules(
        self,
        *,
        routes: Iterable[Route],
        options: RoutePlansOptions,
    ) -> None:
        connections: set[FerryConnection] = set()
        for route in routes:
            for i in range(1, len(route)):
                origin = route[i - 1]
                destination = route[i]
                connection = self._connection_db.from_to_location(origin, destination)
                if isinstance(connection, FerryConnection):
                    connections.add(connection)
        tasks = [self._schedule_getter(c.origin.id, c.destination.id, date=options.date) for c in connections]
        await asyncio.gather(*tasks)

    async def make_route_plans(
        self,
        *,
        routes: Iterable[Route],
        options: RoutePlansOptions,
    ) -> Sequence[RoutePlan]:
        routes = tuple(routes)
        await self._pre_cache_schedules(routes=routes, options=options)
        route_plans = []
        for route in routes:
            await self._add_plan_segment(
                route_plans=route_plans,
                route=route,
                destination_index=1,
                start_time=options.date.replace(hour=0, minute=0, second=0, microsecond=0),
                options=options,
            )
        return route_plans

    async def _add_plan_segment(  # noqa: PLR0913
        self,
        *,
        route_plans: list,
        route: Route,
        destination_index: int,
        start_time: datetime,
        options: RoutePlansOptions,
        segments: list[RoutePlanSegment] | None = None,
    ) -> bool:
        if segments is None:
            segments = []
        result = False
        try:
            if destination_index == len(route):
                if not segments:  # empty list?
                    return False  # can we be here?
                route_plans.append(RoutePlan.from_segments(segments))
                return True
            origin = route[destination_index - 1]
            destination = route[destination_index]
            connection = self._connection_db.from_to_location(origin, destination)
            if isinstance(connection, FerryConnection):
                result = await self._add_ferry_connection(
                    route_plans=route_plans,
                    route=route,
                    destination_index=destination_index,
                    segments=segments,
                    start_time=start_time,
                    options=options,
                    connection=connection,
                )
            if isinstance(connection, CarConnection):
                driving_duration_limit = 6 * 60 * 60
                # Skip driving segments that are more than 6 hours long.
                if not options.show_all and connection.duration > driving_duration_limit:
                    return False
                arrive_time = start_time + timedelta(seconds=connection.duration)
                times = (
                    TimeInterval(
                        type=TimeIntervalType.TRAVEL,
                        start=start_time,
                        end=arrive_time,
                        description=f"Drive {round(connection.distance)} km to {connection.destination.name}",
                    ),
                )
                segments.append(RoutePlanSegment(connection=connection, times=times))
                result = await self._add_plan_segment(
                    route_plans=route_plans,
                    route=route,
                    destination_index=destination_index + 1,
                    segments=segments,
                    start_time=arrive_time,
                    options=options,
                )
        finally:
            delete_start = destination_index - 1
            del segments[delete_start:]
        return result

    async def _add_ferry_connection(  # noqa: C901, PLR0912, PLR0913
        self,
        *,
        route_plans: list,
        route: Route,
        destination_index: int,
        segments: list[RoutePlanSegment],
        start_time: datetime,
        options: RoutePlansOptions,
        connection: FerryConnection,
    ) -> bool:
        result = False
        depature_terminal = connection.origin
        start_day = segments[0].times[0].start.day
        day = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        schedule = await self._schedule_getter(connection.origin.id, connection.destination.id, date=day)
        if not schedule:
            return False
        for sailing in schedule.sailings:
            depart_time = day + datetime_to_timedelta(sailing.departure)
            arrive_time = day + datetime_to_timedelta(sailing.arrival)
            if arrive_time < depart_time:
                arrive_time += timedelta(days=1)
            if not options.show_all and (arrive_time - start_time > timedelta(days=1)) or day.day != start_day:
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
            times = (
                TimeInterval(
                    type=TimeIntervalType.TRAVEL,
                    start=depart_time,
                    end=arrive_time,
                    description=f"Ferry sailing from {connection.origin.name} to {connection.destination.name}",
                ),
            )
            if deadline_time < depart_time:
                description = f"Arrive at {connection.origin.name} "
                if options.buffer > 0:
                    description += f"{options.buffer} minutes "
                description += f"before {deadline_name}"
                times = (
                    TimeInterval(
                        type=TimeIntervalType.WAIT,
                        start=deadline_time,
                        end=depart_time,
                        description=description,
                    ),
                    *times,
                )
            segments.append(
                RoutePlanSegment(
                    connection=connection,
                    times=times,
                    schedule_url=schedule.url,
                ),
            )
            recursion_result = await self._add_plan_segment(
                route_plans=route_plans,
                route=route,
                destination_index=destination_index + 1,
                segments=segments,
                start_time=arrive_time,
                options=options,
            )
            if recursion_result is False:
                break
            delete_start = destination_index - 1
            del segments[delete_start:]
            result = True
            if not options.show_all and sum(1 for s in segments if isinstance(s.connection, FerryConnection)) > 0:
                break
        return result
