from abc import ABC, abstractmethod

from pydantic import BaseModel, field_validator

LocationId = str


class Location(BaseModel, ABC):
    id: LocationId
    name: str
    region: str
    land_group: str | None = None

    def __eq__(self, other: object) -> bool:
        # `isinstance` is not used here because it is much slower and this method
        # is called many times in the recursive route-finding algorithm.
        # Further, we don't expect to compare with anything other than Location objects in the
        # recursive function, so the overhead introduced by `AttributeError` being raised is not relevant.
        try:
            return self.id == other.id  # type: ignore[attr-defined]
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    @abstractmethod
    def map_parameter(self) -> str: ...


class City(Location):
    province: str
    country: str

    @property
    def map_parameter(self) -> str:
        return f"{self.name},{self.province},{self.country}"


class Terminal(Location):
    long_id: str
    info_url: str
    address: str
    coordinates: str
    """String format `"{latitude:float},{longitude:float}"`."""
    veh_close: int | None = None
    """Vehicles check-in close time in minutes."""
    foot_close: int | None = None
    """Foot passengers check-in close time in minutes."""
    res_open: int | None = None
    """Booking check-in open time in minutes."""
    res_close: int | None = None
    """Booking check-in close time in minutes."""
    res_peak_extra: int | None = None
    """Booking check-in extra time required at peak season in minutes."""
    assured_open: int | None = None
    """Assured loading check-in open time in minutes."""
    assured_close: int | None = None
    """Assured loading check-in close time in minutes."""
    hostled_open: int | None = None
    """Hostled vehicles check-in open time in minutes."""
    hostled_close: int | None = None
    """Hostled vehicles check-in close time in minutes."""

    @field_validator("name")
    @classmethod
    def _validate_name(cls, value: str) -> str:
        """Add "terminal" text to name to avoid confusion with cities."""
        if "terminal" in value.lower():
            return value
        if value.endswith(")"):
            return value[:-1] + " Terminal)"
        return value + " (Terminal)"

    @property
    def map_parameter(self) -> str:
        return self.coordinates


class Airport(Location):
    pass


class BusStop(Location):
    pass
