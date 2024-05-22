from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, BaseModel, field_serializer, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
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

CLASS_MAP = {
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


class DataFileInfo(BaseModel):
    path: FilePath
    cls: type[Location | Connection]

    @field_serializer("cls", when_used="json")
    def _serialize_cls(self, value: type[Location | Connection]) -> str:
        return value.__name__

    @field_validator("cls", mode="before")
    @classmethod
    def _validate_cls(cls, value: str | type | None) -> type[Location | Connection]:
        if isinstance(value, str) and value in CLASS_MAP:
            return CLASS_MAP[value]
        if isinstance(value, type) and value in CLASS_MAP.values():
            return value
        msg = (
            f"invalid class name '{value.__name__ if isinstance(value, type) else value}'. "
            f"Valid class names are {', '.join(CLASS_MAP)}"
        )
        raise ValueError(msg)


class DataConfig(BaseModel):
    location_files: tuple[DataFileInfo, ...]
    connection_files: tuple[DataFileInfo, ...]


class SchedulesConfig(BaseModel):
    base_url: str = "https://www.bcferries.com/routes-fares/schedules/daily/"
    cache_dir: DirectoryPath = Path("./data/schedule_cache")
    cache_ahead_days: int = 3
    refresh_interval: int = 60 * 60 * 24  # 24 hours


class Config(BaseSettings):
    data: DataConfig
    schedules: SchedulesConfig = SchedulesConfig()

    model_config = SettingsConfigDict(yaml_file="config.yaml")

    @classmethod
    def settings_customise_sources(  # noqa: PLR0913
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),
        )
