from ferry_planner.config import DBProvider

from .abc import BaseDB
from .d1 import CloudflareD1DB
from .json_files import JsonFileDB

__all__ = (
    "BaseDB",
    "CloudflareD1DB",
    "JsonFileDB",
)

DB_PROVIDERS: dict[DBProvider, type[BaseDB]] = {
    "json_files": JsonFileDB,
    "cloudflare_d1": CloudflareD1DB,
}


def get_db_class(provider_name: DBProvider) -> type[BaseDB]:
    if provider_name in DB_PROVIDERS:
        return DB_PROVIDERS[provider_name]
    msg = f"unsupported DB provider: {provider_name}"
    raise ValueError(msg)
