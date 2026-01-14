import logging
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal, TypeVar
from zoneinfo import ZoneInfo

from pydantic import AfterValidator, BaseModel, ImportString, field_serializer, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
    YamlConfigSettingsSource,
)

from ferry_planner.connection import AirConnection, BusConnection, CarConnection, Connection, FerryConnection
from ferry_planner.location import Airport, BusStop, City, Location, Terminal

if TYPE_CHECKING:
    from importlib.abc import Traversable


def check_is_file(path: "Traversable", /) -> "Traversable":
    if not path.is_file():
        msg = f"path '{path}' is not a file"
        raise ValueError(msg)
    return path


def check_is_dir(path: "Traversable", /) -> "Traversable":
    if not path.is_dir():
        msg = f"path '{path}' is not a directory"
        raise ValueError(msg)
    return path


FilePath = Annotated["Traversable", AfterValidator(check_is_file)]
DirectoryPath = Annotated["Traversable", AfterValidator(check_is_dir)]
DataFileT = TypeVar("DataFileT", Location, Connection)
DBProvider = Literal["json_files", "cloudflare_d1"]

DATA_MODEL_CLASS_MAP = {
    cls.__name__: cls
    for cls in (
        Airport,
        BusStop,
        City,
        Terminal,
        AirConnection,
        BusConnection,
        CarConnection,
        FerryConnection,
    )
}


class DataFileInfo[DataFileT](BaseModel):
    path: FilePath
    cls: type[DataFileT] | ImportString

    @field_serializer("cls", when_used="json")
    def _serialize_cls(self, value: type[Location | Connection]) -> str:
        return value.__name__

    @field_validator("cls", mode="before")
    @classmethod
    def _validate_cls(cls, value: str | type | None) -> type[Location | Connection]:
        if isinstance(value, str) and value in DATA_MODEL_CLASS_MAP:
            return DATA_MODEL_CLASS_MAP[value]
        if isinstance(value, type) and issubclass(value, tuple(DATA_MODEL_CLASS_MAP.values())):
            return value
        msg = (
            f"invalid class name '{value.__name__ if isinstance(value, type) else value}'. "
            f"Valid class names are {', '.join(DATA_MODEL_CLASS_MAP)}"
        )
        raise ValueError(msg)


RESOURCE_DIR = resources.files("ferry_planner.data")
DEFAULT_DATA_FILES = {
    "locations": (
        DataFileInfo(
            path=RESOURCE_DIR / "cities.json",
            cls=City,
        ),
        DataFileInfo(
            path=RESOURCE_DIR / "terminals.json",
            cls=Terminal,
        ),
    ),
    "connections": (
        DataFileInfo(
            path=RESOURCE_DIR / "car_connections.json",
            cls=CarConnection,
        ),
        DataFileInfo(
            path=RESOURCE_DIR / "ferry_connections.json",
            cls=FerryConnection,
        ),
    ),
}


class DataConfig(BaseModel):
    location_files: tuple[DataFileInfo[Location], ...] = DEFAULT_DATA_FILES["locations"]
    connection_files: tuple[DataFileInfo[Connection], ...] = DEFAULT_DATA_FILES["connections"]


class SchedulesConfig(BaseModel):
    db_provider: DBProvider = "json_files"
    base_url: str = "https://www.bcferries.com/routes-fares/schedules/daily/"
    cache_dir: DirectoryPath = Path("./data/schedule_cache")
    cache_ahead_days: int = 1
    refresh_interval_seconds: int = 24 * 60 * 60  # 24 hours


class Config(BaseSettings):
    timezone: ZoneInfo = ZoneInfo("America/Vancouver")
    log_level: ImportString | int = logging.INFO
    schedules: SchedulesConfig = SchedulesConfig()
    data: DataConfig

    model_config = SettingsConfigDict(env_file=".env", toml_file="config.toml", yaml_file="config.yaml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
        )


# This line avoids using a "type: ignore" comment,
# using `config = Config()` would require one as it does not pass type checking.
# Values are still loaded from the config file because
# `Config` inherits from `BaseSettings` instead of `BaseModel`.
# See https://github.com/pydantic/pydantic-settings/issues/108
# and https://github.com/pydantic/pydantic-settings/issues/201
CONFIG = Config.model_validate({})
