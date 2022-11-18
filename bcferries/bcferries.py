import json
import os
import time
from datetime import datetime, timedelta
from threading import Thread
from typing import Optional

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


def load_data(path: str):
    with open(path) as file:
        data = json.load(file)
    add_locations(data.get('terminals'), Terminal)
    add_locations(data.get('cities'), City)
    add_connections(data.get('car_connections_terminal_terminal'), CarConnection)
    add_connections(data.get('car_connections_city_terminal'), CarConnection)
    add_connections(data.get('car_connections_city_city'), CarConnection)
    add_connections(data.get('ferry_connections'), FerryConnection)
    add_connections(data.get('air_connections'), AirConnection)
    add_connections(data.get('bus_connections'), BusConnection)


def add_locations(new_locations: dict[LocationId, dict], cls: type[Location]):
    if not new_locations:
        return
    for location_id, location_info in new_locations.items():
        location_info['id'] = location_id
        location = cls.parse_obj(location_info)
        locations[location_id] = location


def add_connections(new_connections: dict[ConnectionId, dict], cls: type[Connection]):
    if not new_connections:
        return
    for connection_id, connection_info in new_connections.items():
        connection_info['id'] = connection_id
        add_connection(connection_id, connection_info, cls)
    # add reverse connections
    for connection_id, connection_info in new_connections.items():
        id_from, id_to = connection_id.split('-')
        connection_id = f'{id_to}-{id_from}'
        if not connections.get(connection_id):
            connection_info['id'] = connection_id
            add_connection(connection_id, connection_info, cls)


def add_connection(connection_id: ConnectionId, connection_info: dict, cls: type[Connection]):
    origin_id, destination_id = connection_id.split('-')
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
    current_route: Optional[list[LocationId]] = None,
    dead_ends: Optional[list[ConnectionId]] = None,
    lands: Optional[list[str]] = None,
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
    for c in connections_cache.connections.values():
        connection: Connection = c
        if connection.destination.id in current_route or connection.id in dead_ends:
            continue
        if connection.type == ConnectionType.CAR and last_connection_type == ConnectionType.CAR:
            continue  # drive only shortest way between terminals
        if connection.type == ConnectionType.FERRY:
            if connection.destination.land_group and connection.destination.land_group in lands:
                continue
        if connection.type == ConnectionType.FERRY and connection.origin.land_group:
            lands.append(connection.origin.land_group)
        else:
            lands.append('')
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
        connection_id = f'{id_from}-{id_to}'
        connection: FerryConnection = connections[connection_id]  # type: ignore
        if connection.type == ConnectionType.FERRY:
            depature_terminal = connection.origin
            day = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            schedule = schedule_cache.get(id_from, id_to, day)
            for sailing in schedule.sailings:
                depart_time = day + datetime_to_timedelta(
                    datetime.strptime(sailing.depart_time, '%H:%M:%S')
                )
                arrive_time = day + datetime_to_timedelta(
                    datetime.strptime(sailing.arrive_time, '%H:%M:%S')
                )
                if arrive_time < depart_time:
                    arrive_time += timedelta(days=1)
                if not options.show_all and start_time.date() != arrive_time.date():
                    break  # overnight
                if depart_time < start_time:
                    continue
                deadline_name = "departure"
                wait_minutes = 0
                if (
                    options.hostled
                    and depature_terminal.hostled_close
                    and depature_terminal.hostled_close > 0
                ):
                    deadline_name = "hostled vehicles checkin close"
                    wait_minutes = depature_terminal.hostled_close
                if (
                    options.assured
                    and depature_terminal.assured_close
                    and depature_terminal.assured_close > 0
                ):
                    deadline_name = "assured loading checkin close"
                    wait_minutes = depature_terminal.assured_close
                elif (
                    depature_terminal.res_close
                    and depature_terminal.res_close > 0
                    and connection.bookable
                ):
                    # FIXME: depature_terminal.res_peak_extra
                    deadline_name = "booking checkin close"
                    wait_minutes = depature_terminal.res_close
                elif depature_terminal.veh_close and depature_terminal.veh_close > 0:
                    deadline_name = "vehicles checkin close"
                    wait_minutes = depature_terminal.veh_close
                elif depature_terminal.foot_close and depature_terminal.foot_close > 0:
                    deadline_name = "foot passengers checkin close"
                    wait_minutes = depature_terminal.foot_close
                deadline_time = depart_time - timedelta(minutes=wait_minutes)
                deadline_time = deadline_time - timedelta(minutes=options.buffer)
                if deadline_time < start_time:
                    continue
                s = RoutePlanSegment(connection=connection)
                s.schedule_url = schedule.url
                if deadline_time < depart_time:
                    description = f"Arrive at {connection.origin.name} "
                    if options.buffer > 0:
                        description += f"{options.buffer} minutes "
                    description += f"before {deadline_name}"
                    s.times.append(
                        TimeInterval(
                            type=TimeIntervalType.WAIT,
                            start=deadline_time,
                            end=depart_time,
                            description=description,
                        )
                    )
                s.times.append(
                    TimeInterval(
                        type=TimeIntervalType.TRAVEL,
                        start=depart_time,
                        end=arrive_time,
                        description=f"Ferry sailing from {connection.origin.name} to {connection.destination.name}",
                    )
                )
                segments.append(s)
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
                del segments[destination_index - 1:]
                res = True
                if (
                    not options.show_all
                    and sum([1 for s in segments if s.connection.type == ConnectionType.FERRY]) > 0
                ):
                    break
        elif connection.type == ConnectionType.CAR:
            if not options.show_all and connection.duration > 6 * 60 * 60:
                return False
            s = RoutePlanSegment(connection=connection)
            arrive_time = start_time + timedelta(seconds=connection.duration)
            if not options.show_all and start_time.date() != arrive_time.date():
                return False  # overnight
            s.times.append(
                TimeInterval(
                    type=TimeIntervalType.TRAVEL,
                    start=start_time,
                    end=arrive_time,
                    description=f"Drive {round(connection.distance)} km to {connection.destination.name}",
                )
            )
            segments.append(s)
            res = add_plan_segment(
                route,
                destination_index + 1,
                segments,
                arrive_time,
                plans,
                options,
            )
    finally:
        del segments[destination_index - 1:]
    return res


def datetime_to_timedelta(dt: datetime) -> timedelta:
    return timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)


def parse_table(table: Tag) -> list[FerrySailing]:
    sailings = []
    if table:
        for row in table.tbody.find_all('tr'):  # type: ignore
            tds = row.find_all('td')
            if len(tds) < 3:
                continue
            depart_time = datetime.strptime(
                row.find_all('td')[1].text,
                '%I:%M %p',
            ).strftime('%H:%M:%S')
            arrive_time = datetime.strptime(
                row.find_all('td')[2].text,
                '%I:%M %p',
            ).strftime('%H:%M:%S')
            td3 = tds[3].text.strip()
            duration = datetime.strptime(
                td3,
                '%Hh %Mm',
            ).strftime('%H:%M')
            sailing = FerrySailing(
                depart_time=depart_time,
                arrive_time=arrive_time,
                duration=duration,
            )
            sailings.append(sailing)
    return sailings


class ScheduleCache:
    def __init__(self, path: str = 'data/cache'):
        self.path = path
        self.refresh_interval = 60 * 60 * 24
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self.cache = {}
        os.makedirs(self.path, mode=0o755, exist_ok=True)

    def _get_filepath(self, origin: str, destination: str, date: datetime):
        return f'{self.path}/{origin}-{destination}/{date.date()}.json'

    def get(self, origin: str, destination: str, date: datetime) -> FerrySchedule:
        filepath = self._get_filepath(origin, destination, date)
        schedule = self.cache.get(filepath, None)
        if schedule:
            return schedule
        print(filepath)
        if os.path.exists(filepath):
            schedule = FerrySchedule.parse_file(filepath)
            self.cache[filepath] = schedule
            return schedule
        else:
            schedule = self.download_schedule(origin, destination, date)
            self.put(schedule)
            return schedule

    def put(self, schedule: FerrySchedule):
        filepath = self._get_filepath(schedule.origin, schedule.destination, schedule.date)
        self.cache[filepath] = schedule
        dirpath = os.path.dirname(filepath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath, mode=0o755, exist_ok=True)
        with open(filepath, 'w') as file:
            file.write(schedule.json(indent=4))

    def download_schedule(self, origin: str, destination: str, date: datetime) -> FerrySchedule:
        route = f'{origin}-{destination}'
        url = f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        print(f'fetching url: {url}')
        doc = httpx.get(url).text.replace('\u2060', '')
        soup = BeautifulSoup(markup=doc, features='html.parser')
        table = soup.find('table', id='dailyScheduleTableOnward')
        schedule = FerrySchedule(
            date=date,
            origin=origin,
            destination=destination,
            sailings=parse_table(table),  # type: ignore
            url=url,
        )
        return schedule

    def refresh_cache(self):
        ferry_connections = (c for c in connections.values() if c.type == ConnectionType.FERRY)
        cache_ahead_days = 3
        current_date = datetime.now().date()
        current_date = datetime(current_date.year, current_date.month, current_date.day)
        dates = []
        for i in range(cache_ahead_days):
            dates.append(current_date + timedelta(days=i))
        for subdir, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                date = datetime.fromisoformat('.'.join(filename.split('.')[:-1]))
                if date not in dates:
                    os.remove(f'{subdir}/{filename}')
        self.cache = {}
        for connection in ferry_connections:
            for date in dates:
                filepath = self._get_filepath(connection.origin.id, connection.destination.id, date)
                if not os.path.exists(filepath):
                    schedule = self.download_schedule(connection.origin.id, connection.destination.id, date)
                    self.put(schedule)

    def _refresh_task(self):
        while True:
            self.refresh_cache()
            time.sleep(self.refresh_interval)


locations: dict[LocationId, Location] = {}
connections: dict[ConnectionId, Connection] = {}
location_connections: dict[LocationId, ConnectionsCache] = {}
schedule_cache = ScheduleCache()
