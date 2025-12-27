import asyncio
import os
import time
from collections.abc import Iterable
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread

from ferry_planner.connection import FerryConnection
from ferry_planner.location import LocationId
from ferry_planner.schedule import FerrySchedule

from .db import BaseDB


class FileDB(BaseDB):
    def __init__(
        self,
        *,
        ferry_connections: Iterable[FerryConnection],
        base_url: str,
        cache_ahead_days: int,
        refresh_interval: int,
        cache_dir: Path,
        **kwargs: object,
    ) -> None:
        super().__init__(
            ferry_connections=ferry_connections,
            base_url=base_url,
            cache_ahead_days=cache_ahead_days,
            refresh_interval=refresh_interval,
            **kwargs,
        )
        self.cache_dir = cache_dir
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self.cache_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    def _get_filepath(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> Path:
        return self.cache_dir / f"{origin_id}-{destination_id}" / f"{date.date()}.json"

    async def _get_if_exists(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        date: datetime,
    ) -> FerrySchedule | None:
        filepath = self._get_filepath(origin_id, destination_id, date=date)
        if filepath.exists():
            return FerrySchedule.model_validate_json(filepath.read_text(encoding="utf-8"))
        return None

    async def _persist_schedule(self, schedule: FerrySchedule, /) -> None:
        filepath = self._get_filepath(
            schedule.origin,
            schedule.destination,
            date=schedule.date,
        )
        dirpath = filepath.parent
        if not dirpath.exists():
            dirpath.mkdir(mode=0o755, parents=True, exist_ok=True)
        filepath.write_text(schedule.model_dump_json(indent=4, exclude_none=True), encoding="utf-8")

    async def refresh_cache(self) -> None:
        current_date = datetime.now().date()
        current_date = datetime(current_date.year, current_date.month, current_date.day)
        dates = [current_date + timedelta(days=i) for i in range(self.cache_ahead_days)]
        for subdir, _, filenames in os.walk(self.cache_dir):
            for filename in filenames:
                date = datetime.fromisoformat(".".join(filename.split(".")[:-1]))
                if date != current_date and date not in dates:
                    (Path(subdir) / filename).unlink(missing_ok=True)
        # clear memory cache
        self._mem_cache = {}
        # download new schedules
        tasks = []
        for connection in self.ferry_connections:
            for date in dates:
                filepath = self._get_filepath(
                    connection.origin.id,
                    connection.destination.id,
                    date=date,
                )
                if not filepath.exists():
                    tasks.append(
                        asyncio.create_task(
                            self._download_and_save_schedule(
                                connection.origin.id,
                                connection.destination.id,
                                date=date,
                            ),
                        ),
                    )
        downloaded_schedules = sum(await asyncio.gather(*tasks))
        self._log(f"finished refreshing cache, downloaded {downloaded_schedules} schedules")

    def start_refresh_task(self) -> None:
        # Disabled temporarily due to causing too many issues.
        # self._refresh_thread.start()  # noqa: ERA001
        pass

    def _refresh_task(self) -> None:
        while True:
            asyncio.run(self.refresh_cache())
            time.sleep(self.refresh_interval)
