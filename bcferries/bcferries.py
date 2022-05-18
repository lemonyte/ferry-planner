import os
import json
import requests
import typing
import dataclasses
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .classes import (
    AirConnection,
    BaseDataClass,
    BusConnection,
    Connection,
    ConnectionId,
    ConnectionType,
    CarConnection,
    FerryConnection,
    Location,
    LocationId,
    # LocationType,
    Terminal,
    City,
    FerrySailing,
    FerrySchedule,
    TimeInterval,
    Route,
    RoutePlan,
    RoutePlanSegment,
    TimeIntervalType,
    RoutePlanOptions
)

locations: dict[str, Location] = {}
connections: dict[str, Connection] = {}


def load_data(path: str = 'data/data.json'):
    with open(path) as file:
        info = json.load(file)
    add_locations(info.get('terminals'), Terminal)
    add_locations(info.get('cities'), City)
    add_connections(info.get('car_connections'), CarConnection)
    add_connections(info.get('ferry_connections'), FerryConnection)
    add_connections(info.get('air_connections'), AirConnection)
    add_connections(info.get('bus_connections'), BusConnection)


def add_locations(new_locations: dict, obj: Location):
    if not new_locations:
        new_locations = {}
    for location_id, location_info in new_locations.items():
        location_info['id'] = location_id
        location = obj.from_dict(location_info)
        location.connections = {}
        locations[location_id] = location
    # print(f'Added {new_locations.__len__()} {obj.type.name.lower()} locations')


def add_connections(new_connections: dict[ConnectionId, dict], obj: Connection):
    if not new_connections:
        new_connections = {}
    for connection_id, connection_info in new_connections.items():
        connection_info['id'] = connection_id
        add_connection(connection_id, connection_info, obj)
    # add reverse connections
    for connection_id, connection_info in new_connections.items():
        id_from, id_to = connection_id.split('-')
        connection_id = f'{id_to}-{id_from}'
        if not connections.get(connection_id):
            connection_info['id'] = connection_id
            add_connection(connection_id, connection_info, obj)
    # print(f'Added {new_connections.__len__()} {obj.type.name.lower()} connections')


def add_connection(connection_id: ConnectionId, connection_info: dict, obj: BaseDataClass):
    id_from, id_to = connection_id.split('-')
    location_from = locations.get(id_from)
    location_to = locations.get(id_to)
    connection_info['location_from'] = location_from
    connection_info['location_to'] = location_to
    connection = obj.from_dict(connection_info)
    connections[connection_id] = connection
    location_from.connections[id_to] = connection


def find_routes(
    next_point,
    end_point,
    routes: list[Route],
    current_route: list[LocationId] = None,
    dead_ends: list[ConnectionId] = None,
    last_connection_type: ConnectionType = ConnectionType.NONE
):
    if current_route is None:
        current_route = []
    if dead_ends is None:
        dead_ends = []
    current_route.append(next_point)
    if next_point == end_point:
        routes.append(current_route.copy())
        del current_route[-1]
        return True
    next_location = locations[next_point]
    res = False
    for c in next_location.connections.values():
        connection: Connection = c
        if connection.location_to.id in current_route or connection.id in dead_ends:
            continue
        if connection.type == ConnectionType.CAR and connection.type == last_connection_type:
            continue  # drive only shortest way between terminals
        if find_routes(connection.location_to.id, end_point, routes, current_route, dead_ends, connection.type):
            res = True
        else:
            dead_ends.append(connection.id)
    del current_route[-1]
    return res


def make_routes_plans(routes: list[Route], opt: RoutePlanOptions) -> list[RoutePlan]:
    plans: list[RoutePlan] = []
    for route in routes:
        for plan in make_route_plans(route, opt):
            plans.append(plan)
    return plans


def make_route_plans(route: Route, opt: RoutePlanOptions):
    plans = []
    segments = []
    dt = opt.start_time
    add_plan_segment(route, 1, segments, dt, plans, opt)
    return plans


def add_plan_segment(route: Route, destination_index: int, segments: list[RoutePlanSegment], start_time: datetime, plans: list[RoutePlan], options: RoutePlanOptions) -> bool:
    res = False
    if (destination_index == len(route)):
        slen = len(segments)
        if slen == 0:
            return False  # can we be here?
        plan = RoutePlan(segments)
        plans.append(plan)
        return True
    id_from = route[destination_index - 1]
    id_to = route[destination_index]
    connection_id = f"{id_from}-{id_to}"
    connection = connections[connection_id]
    match connection.type:
        case ConnectionType.FERRY:
            depature_terminal: Terminal = connection.location_from
            day = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            schedule = get_schedule(id_from, id_to, day)
            for sailing in schedule.sailings:
                depart_time = day + datetime_to_timedelta(datetime.strptime(sailing.depart_time, '%H:%M:%S'))
                arrive_time = day + datetime_to_timedelta(datetime.strptime(sailing.arrive_time, '%H:%M:%S'))
                if (arrive_time < depart_time):
                    arrive_time += timedelta(days=1)
                if (depart_time < start_time):
                    continue
                deadline_name = "departure"
                wait_minutes = 0
                if options.hostled and depature_terminal.hostled_close and depature_terminal.hostled_close > 0:
                    deadline_name = "hostled vehicles checkin close"
                    wait_minutes = depature_terminal.hostled_close
                if options.assured_load and depature_terminal.assured_close and depature_terminal.assured_close > 0:
                    deadline_name = "assured loading checkin close"
                    wait_minutes = depature_terminal.assured_close
                elif depature_terminal.res_close and depature_terminal.res_close > 0:
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
                deadline_time = deadline_time - timedelta(minutes=options.buffer_time_minutes)
                if (deadline_time < start_time):
                    continue
                new_segments = segments.copy()
                s = RoutePlanSegment(connection)
                if deadline_time < depart_time:
                    description = f"Arrive at {connection.location_from.name} terminal "
                    if options.buffer_time_minutes > 0:
                        description += f"{options.buffer_time_minutes} minutes "
                    description += f"before {deadline_name}"
                    s.times.append(TimeInterval(TimeIntervalType.WAIT, deadline_time, depart_time, description))
                s.times.append(TimeInterval(TimeIntervalType.TRAVEL, depart_time, arrive_time, f"Ferry sailing from {connection.location_from.name} to {connection.location_to.name}"))
                # print(s.times[0].description)
                new_segments.append(s)
                if add_plan_segment(route, destination_index + 1, new_segments, arrive_time, plans, options) is False:
                    break
                res = True
                if options.only_closest_ferry and sum([1 for s in segments if s.connection.type == ConnectionType.FERRY]) > 0:
                    break
        case ConnectionType.CAR:
            s = RoutePlanSegment(connection)
            arrive_time = start_time + timedelta(seconds=connection.duration)
            s.times.append(
                TimeInterval(TimeIntervalType.TRAVEL,
                             start_time,
                             arrive_time,
                             f"Driving {round(connection.distance)} km to {connection.location_to.name}"))
            # print(s.times[0].start.strftime("%H:%M") + " " + s.times[0].description)
            segments.append(s)
            res = add_plan_segment(route, destination_index + 1, segments, arrive_time, plans, options)
    return res


def datetime_to_timedelta(dt):
    return timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)


def parse_table(table: BeautifulSoup) -> list:
    sailings: list[FerrySailing] = []
    if table:
        for row in table.tbody.find_all('tr'):
            depart_time = datetime.strptime(row.find_all('td')[1].text, '%I:%M %p').strftime('%H:%M:%S')
            arrive_time = datetime.strptime(row.find_all('td')[2].text, '%I:%M %p').strftime('%H:%M:%S')
            duration = datetime.strptime(row.find_all('td')[3].div.span.text, '%Hh %Mm').strftime('%H:%M')
            sailing = FerrySailing(depart_time, arrive_time, duration)
            sailings.append(sailing)
    return sailings


def get_schedule(depart_terminal_id: str, arrive_terminal_id: str, date: typing.Union[str, datetime] = None) -> FerrySchedule:
    route = f'{depart_terminal_id}-{arrive_terminal_id}'
    if not date:
        date = datetime.now()
    if isinstance(date, str):
        date = datetime.strptime(date, '%m/%d/%Y')
    date = date.date()
    cache_dir = f"data/cache/{route}"
    filepath = f"{cache_dir}/{date.strftime('%Y-%m-%d')}.json"
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            schedule = FerrySchedule.from_dict(json.loads(file.read()))
            time_difference = datetime.now() - datetime.fromisoformat(schedule.date)
            if time_difference.total_seconds() < 24 * 60 * 60:  # refresh once a day
                return schedule
    # print(f"Requesting schedule {depart_terminal_id}-{arrive_terminal_id}...")
    url = f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
    print(url)
    doc = requests.get(url).text.replace('\u2060', '')
    # print("Parsing schedule...")
    soup = BeautifulSoup(markup=doc, features='html.parser')
    table = soup.find('table', id='dailyScheduleTableOnward')
    schedule = FerrySchedule(date.isoformat(), depart_terminal_id, arrive_terminal_id, parse_table(table))
    os.makedirs(cache_dir, mode=0o666, exist_ok=True)
    with open(filepath, 'w') as file:
        json.dump(dataclasses.asdict(schedule), file, indent=4)
    # print("OK")
    return schedule
