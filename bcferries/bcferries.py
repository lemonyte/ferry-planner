import os
import requests
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import Union

data_template = {
    "date": "",
    "depart_terminal": "",
    "arrive_terminal": "",
    "sailings": []
}

sailing_template = {
    "depart_time": "",
    "arrive_time": "",
    "duration": "",
    "capacity": "",
    "price": ""
}


def parse_table(table: BeautifulSoup) -> list:
    sailings = []
    for row in table.tbody.find_all('tr'):
        sailings.append(sailing_template.copy())
        sailings[-1]['depart_time'] = datetime.strptime(row.find_all('td')[1].text, '%I:%M %p').strftime('%H:%M:%S')
        sailings[-1]['arrive_time'] = datetime.strptime(row.find_all('td')[2].text, '%I:%M %p').strftime('%H:%M:%S')
        duration = datetime.strptime(row.find_all('td')[3].div.span.text, '%Hh %Mm')
        sailings[-1]['duration'] = str(timedelta(hours=duration.hour, minutes=duration.minute))
    return sailings


def get_schedule(depart_terminal_id: str, arrive_terminal_id: str, date: Union[str, datetime] = datetime.now()) -> dict:
    route = f'{depart_terminal_id}-{arrive_terminal_id}'
    if type(date) == str:
        date = datetime.strptime(date, '%m/%d/%Y')
    filepath = f'static/sailings/{route}.json'
    if os.path.exists(filepath):
        with open(filepath) as file:
            data = json.load(file)
            time_difference = datetime.now() - datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
            if time_difference.seconds < (5 * 60):
                return data
    doc = requests.get(f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}&scheduleReturnDate={date.strftime('%m/%d/%Y')}").text.replace('\u2060', '')
    soup = BeautifulSoup(markup=doc, features='html.parser')
    table = soup.find('table', id='dailyScheduleTableOnward')
    data = data_template.copy()
    data['date'] = date.strftime('%Y-%m-%d %H:%M:%S')
    data['depart_terminal'] = depart_terminal_id
    data['arrive_terminal'] = arrive_terminal_id
    data['sailings'] = parse_table(table)
    json.dump(data, open(filepath, 'w'), indent=4)
    return data


def find_routes(next_point, end_point, routes: list = [], current_route: list = []):
    current_route = current_route.copy()
    current_route.append(next_point)
    if next_point in end_point.connections:
        current_route.append(end_point)
        routes.append(current_route)
    else:
        for connection in next_point.connections:
            if connection in current_route:
                continue
            if connection.id == end_point:
                current_route.append(connection)
                routes.append(current_route)
            else:
                find_routes(connection, end_point, current_route.copy(), routes)


def find_connections(next_point, end_point, routes: list = [], current_route: list = []):
    current_route = current_route.copy()
    current_route.append(next_point)
    if next_point in end_point.connections:
        current_route.append(end_point)
        routes.append(current_route)
    else:
        for connection in next_point.connections:
            if connection in current_route:
                continue
            if connection.id == end_point:
                current_route.append(connection)
                routes.append(current_route)
            else:
                find_routes(connection, end_point, current_route.copy(), routes)


class Connection:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)


class Location:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        for connection in self.connections:
            connection = connections[connection]


def load_data(filepath: str, class_template):
    instance_dict = {}
    with open(filepath, 'r') as file:
        data = json.load(file)
    for item in data:
        instance = class_template(item)
        instance_dict[getattr(instance, 'id')] = instance
    return instance_dict


connections = load_data('static/connections.json', Connection)
locations = load_data('static/locations.json', Location)

print(connections)
print(locations)
