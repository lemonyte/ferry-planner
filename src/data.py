import json
from pathlib import Path

from .connection import AirConnection, BusConnection, CarConnection, Connection, ConnectionId, FerryConnection
from .location import City, Location, LocationId, Terminal


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
        location = cls.model_validate(location_info)
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
    connection = cls.model_validate(connection_info)
    connection.origin = origin
    connection.destination = destination
    connections[connection_id] = connection
    if not location_connections.get(origin_id):
        location_connections[origin_id] = ConnectionsCache()
    if isinstance(destination, City):
        location_connections[origin_id].city_connections[destination_id] = connection
    else:
        location_connections[origin_id].connections[destination_id] = connection


class ConnectionsCache:
    def __init__(self) -> None:
        self.connections = {}
        self.city_connections = {}


locations: dict[LocationId, Location] = {}
connections: dict[ConnectionId, Connection] = {}
location_connections: dict[LocationId, ConnectionsCache] = {}
