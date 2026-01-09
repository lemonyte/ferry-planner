import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime

import httpx

from ferry_planner.config import CONFIG
from ferry_planner.connection import FerryConnection
from ferry_planner.location import LocationId
from ferry_planner.schedule import FerrySchedule, ScheduleDownloadError, ScheduleParseError, ScheduleParser


class BaseDB(ABC):
    def __init__(
        self,
        *,
        ferry_connections: Sequence[FerryConnection] | set[FerryConnection] | frozenset[FerryConnection],
        base_url: str | None = None,
        cache_ahead_days: int | None = None,
        refresh_interval: int | None = None,
        **_kwargs: object,
    ) -> None:
        self.ferry_connections = ferry_connections
        self.base_url = base_url or CONFIG.schedules.base_url
        self.cache_ahead_days = cache_ahead_days or CONFIG.schedules.cache_ahead_days
        self.refresh_interval = refresh_interval or CONFIG.schedules.refresh_interval_seconds
        self._mem_cache: dict[tuple[str, str, datetime], FerrySchedule] = {}
        timeout = httpx.Timeout(30.0, pool=None)
        limits = httpx.Limits(max_connections=5)
        self._client = httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=True)
        self._logger = logging.getLogger(self.__class__.__name__)

    def _get_download_url(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> str:
        return f"{self.base_url}{origin_id}-{destination_id}?&scheduleDate={date.strftime('%m/%d/%Y')}"

    @abstractmethod
    async def _get_if_exists(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        date: datetime,
    ) -> FerrySchedule | None: ...

    async def get(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None:
        schedule = self._mem_cache.get((origin_id, destination_id, date))
        if schedule:
            return schedule
        schedule = await self._get_if_exists(origin_id, destination_id, date)
        if schedule:
            return schedule
        schedule = await self.download_schedule(origin_id, destination_id, date=date)
        if schedule:
            await self.put(schedule)
        return schedule

    @abstractmethod
    async def _persist_schedule(self, schedule: FerrySchedule, /) -> None: ...

    async def put(self, schedule: FerrySchedule, /) -> None:
        self._mem_cache[(schedule.origin, schedule.destination, schedule.date)] = schedule
        await self._persist_schedule(schedule)

    async def download_schedule(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None:
        try:
            return await self._download_schedule_async(origin_id, destination_id, date=date)
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

    async def _download_schedule_async(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule:
        url = self._get_download_url(origin_id, destination_id, date=date)
        route = f"{origin_id}-{destination_id}"
        self._logger.info("fetching schedule: %s:%s", route, date.date())
        max_redirects_count = 3
        redirects = []
        while True:
            try:
                response = await self._client.get(url)
            except httpx.HTTPError as exc:
                msg = "failed to download schedule"
                raise ScheduleDownloadError(msg, url=url) from exc
            if not httpx.codes.is_success(response.status_code):
                msg = f"status {response.status_code}"
                raise ScheduleDownloadError(msg, url=url)
            self._logger.info("fetched schedule: %s:%s", route, date.date())
            schedule_parser = ScheduleParser()
            result = schedule_parser.parse_schedule_html(response, date)
            if result.redirect_url:
                if len(redirects) > max_redirects_count:
                    msg = "too many redirects"
                    raise ScheduleDownloadError(msg, url=url)
                if url in redirects:
                    msg = "redirects loop"
                    raise ScheduleDownloadError(msg, url=url)
                url = result.redirect_url
                redirects.append(url)
                continue
            return FerrySchedule(
                date=date,
                origin=origin_id,
                destination=destination_id,
                sailings=tuple(result.sailings),
                url=url,
                notes=result.notes,
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
        if schedule is not None:
            self.put(schedule)
            return True
        return False

    @abstractmethod
    async def refresh_cache(self) -> None: ...

    @abstractmethod
    def start_refresh_task(self) -> None: ...
