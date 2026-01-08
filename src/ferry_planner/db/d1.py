import asyncio
import json
from collections.abc import Iterable
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from ferry_planner.config import CONFIG
from ferry_planner.connection import FerryConnection
from ferry_planner.location import LocationId
from ferry_planner.schedule import FerrySchedule

from .db import BaseDB

if TYPE_CHECKING:
    from js import D1Database


class CloudflareD1DB(BaseDB):
    def __init__(
        self,
        *,
        ferry_connections: Iterable[FerryConnection],
        base_url: str,
        cache_ahead_days: int,
        refresh_interval: int,
        d1_instance: "D1Database",
        **kwargs: object,
    ) -> None:
        super().__init__(
            ferry_connections=ferry_connections,
            base_url=base_url,
            cache_ahead_days=cache_ahead_days,
            refresh_interval=refresh_interval,
            **kwargs,
        )
        self._db = d1_instance

    async def _get_if_exists(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        date: datetime,
    ) -> FerrySchedule | None:
        schedule = await (
            self._db.prepare(
                "SELECT raw_data FROM schedules WHERE origin = ? AND destination = ? AND date = ? LIMIT 1",
            )
            .bind(origin_id, destination_id, date.isoformat())
            .first("raw_data")
        )
        if schedule:
            return FerrySchedule.model_validate_json(schedule)
        return None

    async def _persist_schedule(self, schedule: FerrySchedule, /) -> None:
        await (
            self._db.prepare("INSERT OR REPLACE INTO schedules (raw_data) VALUES (?)")
            .bind(schedule.model_dump_json())
            .run()
        )

    async def refresh_cache(self) -> None:
        current_date = datetime.now(tz=CONFIG.timezone).replace(hour=0, minute=0, second=0, microsecond=0)
        dates = [current_date + timedelta(days=i) for i in range(self.cache_ahead_days)]
        await (
            self._db.prepare(
                "DELETE FROM schedules WHERE date NOT IN (SELECT value FROM json_each(?1))",
            )
            .bind(json.dumps([current_date.isoformat(), *(date.isoformat() for date in dates)]))
            .run()
        )
        # clear memory cache
        self._mem_cache = {}
        # download new schedules
        tasks = [
            asyncio.create_task(
                self._download_and_save_schedule(
                    connection.origin.id,
                    connection.destination.id,
                    date=date,
                ),
            )
            for connection in self.ferry_connections
            for date in dates
        ]
        downloaded_schedules = sum(await asyncio.gather(*tasks))
        self._logger.info("finished refreshing cache, downloaded %d schedules", downloaded_schedules)

    def start_refresh_task(self) -> None:
        """Start a background task to refresh the cache periodically.

        Does nothing for Cloudflare D1 DB, since refreshes are triggered by a cron job.
        """
