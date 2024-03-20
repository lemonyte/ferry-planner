from abc import ABC

from pydantic import BaseModel

from .location import Location, Terminal

ConnectionId = str


class Connection(BaseModel, ABC):
    id: ConnectionId
    origin: Location = None  # type: ignore[None]
    destination: Location = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    distance: float
    fuel: float


class FerryConnection(Connection):
    origin: Terminal = None  # type: ignore[None]
    destination: Terminal = None  # type: ignore[None]
    duration: int = None  # type: ignore[None]
    distance: float = 0.2
    fuel: float = 0.2
    bookable: bool = False


class CarConnection(Connection):
    pass


class AirConnection(Connection):
    pass


class BusConnection(Connection):
    pass
