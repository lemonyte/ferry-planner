# ruff: noqa: DTZ005, DTZ007
from datetime import datetime
from typing import Self

from pydantic import BaseModel, field_validator, model_validator


class RoutesOptions(BaseModel):
    origin: str
    destination: str

    @model_validator(mode="after")
    def _validate_route(self) -> Self:
        if self.origin == self.destination:
            msg = "origin and destination cannot be the same"
            raise ValueError(msg)
        return self


class ScheduleOptions(RoutesOptions):
    date: datetime

    @field_validator("date", mode="before")
    @classmethod
    def _parse_date(cls, value: str | datetime | None) -> datetime:
        if not value:
            value = datetime.now()
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d")
        return value


class RoutePlansOptions(ScheduleOptions):
    show_all: bool = False
    assured: bool = False
    reservation: bool = False
    hostled: bool = False
    buffer: int = 15
