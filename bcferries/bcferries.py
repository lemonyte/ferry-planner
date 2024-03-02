# ruff: noqa: DTZ001, DTZ005, DTZ007
from __future__ import annotations

import asyncio
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread

import httpx
from bs4 import BeautifulSoup, Tag

from .classes import (
    AirConnection,
    BusConnection,
    CarConnection,
    City,
    Connection,
    ConnectionId,
    ConnectionsCache,
    ConnectionType,
    FerryConnection,
    FerrySailing,
    FerrySchedule,
    Location,
    LocationId,
    LocationType,
    Route,
    RoutePlan,
    RoutePlanSegment,
    RoutePlansOptions,
    Terminal,
    TimeInterval,
    TimeIntervalType,
)


def load_data(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    add_locations(data.get("terminals"), Terminal)
    add_locations(data.get("cities"), City)
    add_connections(data.get("car_connections_terminal_terminal"), CarConnection)
    add_connections(data.get("car_connections_city_terminal"), CarConnection)
    add_connections(data.get("car_connections_city_city"), CarConnection)
    add_connections(data.get("ferry_connections"), FerryConnection)
    add_connections(data.get("air_connections"), AirConnection)
    add_connections(data.get("bus_connections"), BusConnection)


def add_locations(new_locations: dict[LocationId, dict], cls: type[Location]) -> None:
    if not new_locations:
        return
    for location_id, location_info in new_locations.items():
        location_info["id"] = location_id
        location = cls.parse_obj(location_info)
        locations[location_id] = location


def add_connections(new_connections: dict[ConnectionId, dict], cls: type[Connection]) -> None:
    if not new_connections:
        return
    for connection_id, connection_info in new_connections.items():
        connection_info["id"] = connection_id
        add_connection(connection_id, connection_info, cls)
    # Add reverse connections.
    for connection_id, connection_info in new_connections.items():
        id_from, id_to = connection_id.split("-")
        connection_id_rev = f"{id_to}-{id_from}"
        if not connections.get(connection_id_rev):
            connection_info["id"] = connection_id_rev
            add_connection(connection_id_rev, connection_info, cls)


def add_connection(connection_id: ConnectionId, connection_info: dict, cls: type[Connection]) -> None:
    origin_id, destination_id = connection_id.split("-")
    try:
        origin = locations[origin_id]
        destination = locations[destination_id]
    except KeyError:
        return
    connection = cls.parse_obj(connection_info)
    connection.origin = origin
    connection.destination = destination
    connections[connection_id] = connection
    if not location_connections.get(origin_id):
        location_connections[origin_id] = ConnectionsCache()
    if destination.type == LocationType.CITY:
        location_connections[origin_id].city_connections[destination_id] = connection
    else:
        location_connections[origin_id].connections[destination_id] = connection


def find_routes(origin_id: str, destination_id: str) -> list[Route]:
    routes = []
    find_routes_recurse(origin_id, destination_id, routes)
    return routes


def find_routes_recurse(
    next_point: str,
    end_point: str,
    routes: list[Route],
    current_route: list[LocationId] | None = None,
    dead_ends: list[ConnectionId] | None = None,
    lands: list[str] | None = None,
    last_connection_type: ConnectionType = ConnectionType.NONE,
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
        if connection.type == ConnectionType.CAR and last_connection_type == ConnectionType.CAR:
            continue  # Drive only shortest way between terminals.
        if (
            connection.type == ConnectionType.FERRY
            and connection.destination.land_group
            and connection.destination.land_group in lands
        ):
            continue
        if connection.type == ConnectionType.FERRY and connection.origin.land_group:
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
            connection.type,
        ):
            res = True
        else:
            dead_ends.append(connection.id)
        del lands[-1]
    del current_route[-1]
    return res


def make_route_plans(routes: list[Route], options: RoutePlansOptions) -> list[RoutePlan]:
    all_plans = []
    for route in routes:
        route_plans = []
        segments = []
        add_plan_segment(route, 1, segments, options.date, route_plans, options)
        all_plans.extend(route_plans)
    return all_plans


def add_plan_segment(
    route: Route,
    destination_index: int,
    segments: list[RoutePlanSegment],
    start_time: datetime,
    plans: list[RoutePlan],
    options: RoutePlansOptions,
) -> bool:
    res = False
    try:
        if destination_index == len(route):
            if not segments:  # empty list?
                return False  # can we be here?
            plan = RoutePlan()
            plan.init(segments)
            plans.append(plan)
            return True
        id_from = route[destination_index - 1]
        id_to = route[destination_index]
        connection_id = f"{id_from}-{id_to}"
        connection = connections[connection_id]
        if connection.type == ConnectionType.FERRY and isinstance(connection, FerryConnection):
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
            )
        if connection.type == ConnectionType.CAR and isinstance(connection, CarConnection):
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
            )
    finally:
        delete_start = destination_index - 1
        del segments[delete_start:]
    return res


def add_ferry_connection(
    route: Route,
    destination_index: int,
    segments: list[RoutePlanSegment],
    start_time: datetime,
    plans: list[RoutePlan],
    options: RoutePlansOptions,
    id_from: str,
    id_to: str,
    connection: FerryConnection,
) -> bool:
    res = False
    depature_terminal = connection.origin
    day = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    schedule = schedule_cache.get(id_from, id_to, day)
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
            # TODO: depature_terminal.res_peak_extra
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
            )
            is False
        ):
            break
        delete_start = destination_index - 1
        del segments[delete_start:]
        res = True
        if not options.show_all and sum(1 for s in segments if s.connection.type == ConnectionType.FERRY) > 0:
            break
    return res


def datetime_to_timedelta(value: datetime) -> timedelta:
    return timedelta(hours=value.hour, minutes=value.minute, seconds=value.second)


def parse_table(table: Tag) -> list[FerrySailing]:
    sailings = []
    sailing_row_min_td_count = 3
    if table and table.tbody:
        for row in table.tbody.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) < sailing_row_min_td_count:
                continue
            depart_time = datetime.strptime(
                row.find_all("td")[1].text,
                "%I:%M %p",
            ).strftime("%H:%M:%S")
            arrive_time = datetime.strptime(
                row.find_all("td")[2].text,
                "%I:%M %p",
            ).strftime("%H:%M:%S")
            td3 = tds[3].text.strip()
            duration = datetime.strptime(
                td3,
                "%Hh %Mm",
            ).strftime("%H:%M")
            sailing = FerrySailing(
                depart_time=depart_time,
                arrive_time=arrive_time,
                duration=duration,
            )
            sailings.append(sailing)
    return sailings


class ScheduleCache:
    def __init__(self, path: Path = Path("data/cache")) -> None:
        self.path = path
        self.refresh_interval = 60 * 60 * 24
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self.cache = {}
        self.path.mkdir(mode=0o755, parents=True, exist_ok=True)

    def _get_filepath(self, origin: str, destination: str, date: datetime) -> Path:
        return self.path / f"{origin}-{destination}" / f"{date.date()}.json"

    def get(self, origin: str, destination: str, date: datetime) -> FerrySchedule | None:
        filepath = self._get_filepath(origin, destination, date)
        schedule = self.cache.get(filepath, None)
        if schedule:
            return schedule
        if filepath.exists():
            schedule = FerrySchedule.parse_file(filepath)
            self.cache[filepath] = schedule
            return schedule
        schedule = self.download_schedule(origin, destination, date)
        if schedule:
            self.put(schedule)
        return schedule

    def put(self, schedule: FerrySchedule) -> None:
        filepath = self._get_filepath(schedule.origin, schedule.destination, schedule.date)
        self.cache[filepath] = schedule
        dirpath = filepath.parent
        if not dirpath.exists():
            dirpath.mkdir(mode=0o755, parents=True, exist_ok=True)
        filepath.write_text(schedule.json(indent=4), encoding="utf-8")

    def download_schedule(self, origin: str, destination: str, date: datetime) -> FerrySchedule | None:
        route = f"{origin}-{destination}"
        url = (
            f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        )
        print(f"fetching url: {url}")
        try:
            doc = httpx.get(url).text.replace("\u2060", "")
        except httpx.ConnectTimeout as exc:
            print(exc)
            return None
        return self.parse_schedule_html(origin, destination, date, url, doc)

    async def download_schedule_async(
        self,
        origin: str,
        destination: str,
        date: datetime,
        *,
        client: httpx.AsyncClient,
    ) -> FerrySchedule:
        route = f"{origin}-{destination}"
        url = (
            f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        )
        print(f"[INFO] fetching schedule: {route}:{date.date()}")
        doc = (await client.get(url)).text.replace("\u2060", "")
        print(f"[INFO] fetched schedule: {route}:{date.date()}")
        return self.parse_schedule_html(origin, destination, date, url, doc)

    def parse_schedule_html(
        self,
        origin: str,
        destination: str,
        date: datetime,
        url: str,
        html: str,
    ) -> FerrySchedule:
        soup = BeautifulSoup(markup=html, features="html.parser")
        table = soup.find("table", id="dailyScheduleTableOnward")
        sailings = parse_table(table) if isinstance(table, Tag) else []
        return FerrySchedule(
            date=date,
            origin=origin,
            destination=destination,
            sailings=sailings,
            url=url,
        )

    async def _download_and_save_schedule(
        self,
        connection: Connection,
        date: datetime,
        *,
        client: httpx.AsyncClient,
    ) -> None:
        schedule = await self.download_schedule_async(
            connection.origin.id,
            connection.destination.id,
            date,
            client=client,
        )
        if schedule:
            self.put(schedule)

    async def refresh_cache(self) -> None:
        ferry_connections = (c for c in connections.values() if c.type == ConnectionType.FERRY)
        cache_ahead_days = 3
        current_date = datetime.now().date()
        current_date = datetime(current_date.year, current_date.month, current_date.day)
        dates = [current_date + timedelta(days=i) for i in range(cache_ahead_days)]
        for subdir, _, filenames in os.walk(self.path):
            for filename in filenames:
                date = datetime.fromisoformat(".".join(filename.split(".")[:-1]))
                if date not in dates:
                    (Path(subdir) / filename).unlink(missing_ok=True)
        # clear memory cache
        self.cache = {}
        # download new schedules
        tasks = []
        async with httpx.AsyncClient() as client:
            for connection in ferry_connections:
                for date in dates:
                    filepath = self._get_filepath(connection.origin.id, connection.destination.id, date)
                    if not filepath.exists():
                        tasks.append(
                            asyncio.ensure_future(
                                self._download_and_save_schedule(
                                    connection,
                                    date,
                                    client=client,
                                ),
                            ),
                        )
            await asyncio.gather(*tasks)
        print("[INFO] finished refreshing cache")

    def start_refresh_thread(self) -> None:
        self._refresh_thread.start()

    def _refresh_task(self) -> None:
        while True:
            asyncio.run(self.refresh_cache())
            time.sleep(self.refresh_interval)


locations: dict[LocationId, Location] = {}
connections: dict[ConnectionId, Connection] = {}
location_connections: dict[LocationId, ConnectionsCache] = {}
schedule_cache = ScheduleCache()
