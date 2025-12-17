from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel, ValidationInfo, model_validator

from ferry_planner.location import Airport, BusStop, Location, Terminal

if TYPE_CHECKING:
    from ferry_planner.data import LocationDB

ConnectionId = str

DataT = TypeVar("DataT", Any, dict[str, Any])
OriginT_co = TypeVar("OriginT_co", bound="Location", covariant=True)
DestinationT_co = TypeVar("DestinationT_co", bound="Location", covariant=True)


class ConnectionType(Enum):
    FERRY = "FERRY"
    """Ferry connection."""
    CAR = "CAR"
    """Car connection."""
    BUS = "BUS"
    """Bus connection."""
    AIR = "AIR"
    """Air connection."""


class Connection(BaseModel, ABC, Generic[OriginT_co, DestinationT_co]):
    id: ConnectionId
    origin: OriginT_co
    destination: DestinationT_co
    duration: int
    """Duration in seconds."""
    distance: float
    """Distance in kilometers."""
    fuel: float
    """Fuel usage in litres, assuming an efficiency of approximately 10 litres per 100 km."""
    type: ConnectionType

    def __eq__(self, other: object) -> bool:
        # `isinstance` is not used here because it is much slower and this method
        # is called many times in the recursive route-finding algorithm.
        # Further, we don't expect to compare with anything other than Connection objects in the
        # recursive function, so the overhead introduced by `AttributeError` being raised is not relevant.
        try:
            return self.id == other.id  # type: ignore[attr-defined]
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    @model_validator(mode="before")
    @classmethod
    def _validate_origin_destination(cls, data: Any, info: ValidationInfo) -> Any:  # noqa: ANN401 Needed for Pydantic validators.
        if isinstance(data, dict):
            origin = data.get("origin")
            destination = data.get("destination")
            if isinstance(origin, Location) and isinstance(destination, Location):
                # Skip validation if origin and destination are already Location instances.
                return data
            if not isinstance(info.context, dict) or "location_db" not in info.context:
                msg = "location_db is required in context for origin and destination validation"
                raise ValueError(msg)
            location_db: LocationDB = info.context["location_db"]
            if not isinstance(origin, Location) and "origin_id" in data:
                data["origin"] = location_db.by_id(data["origin_id"])
            if not isinstance(destination, Location) and "destination_id" in data:
                data["destination"] = location_db.by_id(data["destination_id"])
        return data


class FerryConnection(Connection[Terminal, Terminal]):
    duration: int = -1
    """Duration for ferry connections is known only from schedule data, and can vary.
    Use the `FerrySailing.duration` attribute to get the actual duration for a specific sailing.
    """
    distance: float = 0.2
    fuel: float = 0.2
    """Fuel usage is estimated for boarding and unboarding only, not for the actual sailing."""
    bookable: bool = False
    from_reverse: bool = False
    """Internal attribute used to indicate that this connection was generated from its reverse connection."""
    type: ConnectionType = ConnectionType.FERRY


# Car connections can be between locations of any type, so we use the base class Location for both type parameters.
class CarConnection(Connection[Location, Location]):
    type: ConnectionType = ConnectionType.CAR


class AirConnection(Connection[Airport, Airport]):
    type: ConnectionType = ConnectionType.AIR


class BusConnection(Connection[BusStop, BusStop]):
    type: ConnectionType = ConnectionType.BUS
