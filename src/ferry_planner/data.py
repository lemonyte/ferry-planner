from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

from pydantic import BaseModel

from ferry_planner.connection import (
    AirConnection,
    BusConnection,
    CarConnection,
    Connection,
    ConnectionId,
    FerryConnection,
)
from ferry_planner.location import City, Location, LocationId, Terminal

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, MutableMapping

ModelT = TypeVar("ModelT", bound=BaseModel)
LocationT = TypeVar("LocationT", bound=Location)
OriginT = TypeVar("OriginT", bound=Location)
DestinationT = TypeVar("DestinationT", bound=Location)


class LocationNotFoundError(Exception):
    def __init__(self, location_id: LocationId, *args: Iterable) -> None:
        self.location_id = location_id
        super().__init__(f"Location not found with ID {location_id}", *args)


class ConnectionNotFoundError(Exception):
    def __init__(self, connection_id: ConnectionId, *args: Iterable) -> None:
        self.connection_id = connection_id
        super().__init__(f"Connection not found with ID {connection_id}", *args)


def load_from_json(file: Path, /, *, data_type: type[ModelT]) -> Iterator[ModelT]:
    data = json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"Data file '{file}' must contain a dictionary"
        raise TypeError(msg)
    return (data_type.model_validate(item) for item in data.values())


class LocationDB:
    def __init__(self, locations: Iterable[Location], /) -> None:
        self._locations: dict[LocationId, Location] = {location.id: location for location in locations}

    @classmethod
    def from_files(cls) -> LocationDB:
        locations = []
        locations.extend(load_from_json(Path("data/cities.json"), data_type=City))
        locations.extend(load_from_json(Path("data/terminals.json"), data_type=Terminal))
        return cls(locations)

    def dict(self) -> MutableMapping[LocationId, Location]:
        return self._locations.copy()

    def all(self) -> Iterator[Location]:
        yield from self._locations.values()

    def by_id(self, location_id: LocationId, /) -> Location:
        location = self._locations.get(location_id)
        if location is None:
            raise LocationNotFoundError(location_id)
        return location


class ConnectionDB:
    def __init__(self, connections: Iterable[Connection], /) -> None:
        self._connections: dict[ConnectionId, Connection] = {connection.id: connection for connection in connections}

    @classmethod
    def from_files(cls, *, location_db: LocationDB) -> ConnectionDB:
        files: tuple[tuple[Path, type[Connection]], ...] = (
            (Path("data/car_connections.json"), CarConnection),
            (Path("data/ferry_connections.json"), FerryConnection),
            (Path("data/air_connections.json"), AirConnection),
            (Path("data/bus_connections.json"), BusConnection),
        )
        connections = []
        for file, connection_type in files:
            if file.exists():
                data = json.loads(file.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    msg = f"Data file {file} must contain a dictionary"
                    raise ValueError(msg)
                connections.extend(
                    (
                        connection_type.model_validate(obj, context={"location_db": location_db})
                        for obj in data.values()
                    ),
                )
        return cls(connections)

    def dict(self) -> MutableMapping[ConnectionId, Connection[Location, Location]]:
        return self._connections.copy()

    def all(self) -> Iterator[Connection[Location, Location]]:
        """Get all connections."""
        yield from self._connections.values()

    def by_id(self, connection_id: ConnectionId, /) -> Connection[Location, Location]:
        """Get a connection by its ID."""
        return self._connections[connection_id]

    def from_location(self, location: OriginT, /) -> Iterator[Connection[OriginT, Location]]:
        """Get all connections from a location."""
        return (connection for connection in self._connections.values() if connection.origin.id == location.id)

    def to_location(self, location: DestinationT, /) -> Iterator[Connection[Location, DestinationT]]:
        """Get all connections to a location."""
        return (connection for connection in self._connections.values() if connection.destination.id == location.id)

    def from_to_location(self, origin: OriginT, destination: DestinationT, /) -> Connection[OriginT, DestinationT]:
        """Get a connection between two locations."""
        connection_id = f"{origin.id}-{destination.id}"
        connection = self._connections.get(connection_id)
        if connection is None:
            raise ConnectionNotFoundError(connection_id)
        return connection

    def with_location(
        self,
        location: LocationT,
        /,
    ) -> Iterator[Connection[Location, LocationT] | Connection[LocationT, Location]]:
        """Get all connections that include a location as either the origin or destination."""
        return (
            connection
            for connection in self._connections.values()
            if location.id in {connection.origin.id, connection.destination.id}
        )

    def with_locations(
        self,
        origin: OriginT,
        destination: DestinationT,
        /,
    ) -> Iterator[Connection[OriginT, DestinationT] | Connection[DestinationT, OriginT]]:
        """Get connections that include two locations as either the origin or destination."""
        return (
            connection
            for connection in self._connections.values()
            if origin.id in {connection.origin.id, connection.destination.id}
            and destination.id in {connection.origin.id, connection.destination.id}
        )
