import logging
from pathlib import Path
from typing import Annotated, Generic, TypeVar
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


def check_is_file(path: Path, /) -> Path:
    if not path.is_file():
        msg = f"path '{path}' is not a file"
        raise ValueError(msg)
    return path


def check_is_dir(path: Path, /) -> Path:
    if not path.is_dir():
        msg = f"path '{path}' is not a directory"
        raise ValueError(msg)
    return path


FilePath = Annotated[Path, AfterValidator(check_is_file)]
DirectoryPath = Annotated[Path, AfterValidator(check_is_dir)]
DataFileT = TypeVar("DataFileT", Location, Connection)

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


class DataFileInfo(BaseModel, Generic[DataFileT]):
    path: FilePath
    cls: type[DataFileT]

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


class DataConfig(BaseModel):
    location_files: tuple[DataFileInfo[Location], ...]
    connection_files: tuple[DataFileInfo[Connection], ...]


class SchedulesConfig(BaseModel):
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
