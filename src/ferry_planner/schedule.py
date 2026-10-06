import asyncio
import logging
import os
import time
from collections.abc import Iterable
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread
from typing import Protocol
from weakref import WeakKeyDictionary

import httpx
from pydantic import BaseModel

from ferry_planner.config import CONFIG
from ferry_planner.connection import FerryConnection
from ferry_planner.gtfs import GtfsFeed
from ferry_planner.location import LocationId

NO_SAILINGS_NOTE = "No sailings found"
SCHEDULE_NOT_POSTED_NOTE = "Seasonal schedules have not been posted for these dates"
FEED_RETRY_SECONDS = 60
"""Time to wait before downloading the feed again after failing to."""


class FerrySailing(BaseModel):
    departure: datetime
    arrival: datetime
    duration: int
    """Duration in seconds."""
    # TODO @lemonyte: price: float  # noqa: FIX002
    """Price in Canadian dollars (CAD)."""
    notes: tuple[str, ...] = ()
    """Notes or comments posted about this sailing."""

    def __hash__(self) -> int:
        return hash((self.departure, self.arrival, self.duration, self.notes))


class FerrySchedule(BaseModel):
    date: datetime
    origin: LocationId
    destination: LocationId
    sailings: tuple[FerrySailing, ...]
    url: str
    notes: tuple[str, ...] = ()
    """Notes or comments posted about this schedule."""


class ScheduleGetter(Protocol):
    async def __call__(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None: ...


class ScheduleDownloadError(Exception):
    def __init__(self, msg: str, /, *args: Iterable, url: str) -> None:
        self.url = url
        super().__init__(f"error downloading schedule at {url}: {msg}", *args)


class ScheduleParseError(Exception):
    def __init__(self, msg: str, /, *args: Iterable, url: str) -> None:
        self.url = url
        super().__init__(f"error parsing schedule at {url}: {msg}", *args)


class ScheduleDB:
    def __init__(  # noqa: PLR0913
        self,
        *,
        ferry_connections: Iterable[FerryConnection],
        schedule_base_url: str | None = None,
        gtfs_url: str | None = None,
        cache_dir: Path | None = None,
        cache_ahead_days: int | None = None,
        refresh_interval: int | None = None,
    ) -> None:
        self.ferry_connections = ferry_connections
        self.schedule_base_url = schedule_base_url or CONFIG.schedules.schedule_base_url
        self.gtfs_url = gtfs_url or CONFIG.schedules.gtfs_url
        self.cache_dir = cache_dir or CONFIG.schedules.cache_dir
        self.cache_ahead_days = cache_ahead_days or CONFIG.schedules.cache_ahead_days
        self.refresh_interval = refresh_interval or CONFIG.schedules.refresh_interval_seconds
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self._mem_cache = {}
        self._terminals = {
            terminal.id: terminal
            for connection in ferry_connections
            for terminal in (connection.origin, connection.destination)
        }
        self._gtfs_feed: GtfsFeed | None = None
        # Time after which the feed is downloaded again.
        self._gtfs_feed_expiry = float("-inf")
        # Prevent the feed from being downloaded more than once when several schedules are requested at once.
        # A lock only works in one event loop, and the refresh thread runs its own.
        self._gtfs_feed_locks: WeakKeyDictionary[asyncio.AbstractEventLoop, asyncio.Lock] = WeakKeyDictionary()
        self.cache_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
        timeout = httpx.Timeout(30.0, pool=None)
        limits = httpx.Limits(max_connections=5)
        self._client = httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=True)
        self._logger = logging.getLogger(self.__class__.__name__)

    def _get_schedule_url(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> str:
        return f"{self.schedule_base_url}{origin_id}-{destination_id}?&scheduleDate={date.strftime('%m/%d/%Y')}"

    def _get_filepath(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> Path:
        return self.cache_dir / f"{origin_id}-{destination_id}" / f"{date.date()}.json"

    async def get(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None:
        filepath = self._get_filepath(origin_id, destination_id, date=date)
        schedule = self._mem_cache.get(filepath)
        if schedule is None and filepath.exists():
            schedule = FerrySchedule.model_validate_json(filepath.read_text(encoding="utf-8"))
            self._mem_cache[filepath] = schedule
        # Schedules without sailings can gain them when the feed is updated, so only those with sailings are cached.
        if schedule and schedule.sailings:
            return schedule
        schedule = await self.download_schedule(origin_id, destination_id, date=date)
        if schedule and schedule.sailings:
            self.put(schedule)
        return schedule

    def put(self, schedule: FerrySchedule, /) -> None:
        filepath = self._get_filepath(
            schedule.origin,
            schedule.destination,
            date=schedule.date,
        )
        self._mem_cache[filepath] = schedule
        dirpath = filepath.parent
        if not dirpath.exists():
            dirpath.mkdir(mode=0o755, parents=True, exist_ok=True)
        filepath.write_text(schedule.model_dump_json(indent=4, exclude_none=True), encoding="utf-8")

    async def download_schedule(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None:
        try:
            return await self._get_gtfs_schedule(origin_id, destination_id, date=date)
        except (ScheduleDownloadError, ScheduleParseError) as exc:
            msg = "failed to parse schedule" if isinstance(exc, ScheduleParseError) else "failed to download schedule"
            self._logger.exception(
                "%s %s-%s:%s from %s",
                msg,
                origin_id,
                destination_id,
                date.date(),
                exc.url,
            )
            return None

    async def _get_gtfs_feed(self) -> GtfsFeed:
        async with self._gtfs_feed_locks.setdefault(asyncio.get_running_loop(), asyncio.Lock()):
            if time.monotonic() > self._gtfs_feed_expiry:
                try:
                    self._gtfs_feed = await self._download_gtfs_feed()
                except (ScheduleDownloadError, ScheduleParseError):
                    # Schedules requested in the meantime do not each wait for another attempt.
                    self._gtfs_feed_expiry = time.monotonic() + FEED_RETRY_SECONDS
                    if self._gtfs_feed is None:
                        raise
                    self._logger.exception("failed to update GTFS feed, using the previous one")
                else:
                    self._gtfs_feed_expiry = time.monotonic() + self.refresh_interval
            if self._gtfs_feed is None:
                msg = "previous attempt failed"
                raise ScheduleDownloadError(msg, url=self.gtfs_url)
            return self._gtfs_feed

    async def _download_gtfs_feed(self) -> GtfsFeed:
        self._logger.info("fetching GTFS feed")
        try:
            response = await self._client.get(self.gtfs_url)
        except httpx.HTTPError as exc:
            msg = "failed to download GTFS feed"
            raise ScheduleDownloadError(msg, url=self.gtfs_url) from exc
        if not httpx.codes.is_success(response.status_code):
            msg = f"status {response.status_code}"
            raise ScheduleDownloadError(msg, url=self.gtfs_url)
        locations = {}
        for terminal in self._terminals.values():
            latitude, longitude = terminal.coordinates.split(",")
            locations[terminal.id] = (float(latitude), float(longitude))
        try:
            feed = GtfsFeed(response.content, locations=locations, timezone=CONFIG.timezone)
        except Exception as exc:
            msg = "failed to parse GTFS feed"
            raise ScheduleParseError(msg, url=self.gtfs_url) from exc
        self._logger.info("fetched GTFS feed")
        return feed

    async def _get_gtfs_schedule(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule:
        feed = await self._get_gtfs_feed()
        # The feed can list sailings for dates it does not cover, but those are not reliable.
        if not feed.covers(date.date()):
            sailings = ()
            notes = (SCHEDULE_NOT_POSTED_NOTE,)
        else:
            sailings = tuple(
                FerrySailing(
                    departure=sailing.departure,
                    arrival=sailing.arrival,
                    duration=int((sailing.arrival - sailing.departure).total_seconds()),
                    notes=(f"Via {', '.join(self._terminals[stop].name for stop in sailing.stops)}",)
                    if sailing.stops
                    else (),
                )
                for sailing in feed.sailings(origin_id, destination_id, date.date())
            )
            notes = () if sailings else (NO_SAILINGS_NOTE,)
        return FerrySchedule(
            date=date,
            origin=origin_id,
            destination=destination_id,
            sailings=sailings,
            url=self._get_schedule_url(origin_id, destination_id, date=date),
            notes=notes,
        )

    async def _download_and_save_schedule(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> bool:
        schedule = await self.download_schedule(
            origin_id,
            destination_id,
            date=date,
        )
        if schedule is not None and schedule.sailings:
            self.put(schedule)
        return schedule is not None

    async def refresh_cache(self) -> None:
        current_date = datetime.now(tz=CONFIG.timezone).replace(hour=0, minute=0, second=0, microsecond=0)
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
        self._logger.info("finished refreshing cache, downloaded %d schedules", downloaded_schedules)

    def start_refresh_thread(self) -> None:
        # Disabled temporarily due to causing too many issues.
        if False:
            self._refresh_thread.start()

    def _refresh_task(self) -> None:
        while True:
            asyncio.run(self.refresh_cache())
            time.sleep(self.refresh_interval)
