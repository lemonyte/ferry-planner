# ruff: noqa: DTZ001, DTZ005, DTZ007
import asyncio
import os
import time
from collections.abc import Callable, Iterable, Iterator
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread

import httpx
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from ferry_planner.connection import Connection, FerryConnection
from ferry_planner.location import LocationId, Terminal
from ferry_planner.util import datetime_to_timedelta


class FerrySailing(BaseModel):
    departure: datetime
    arrival: datetime
    duration: int
    """Duration in seconds."""
    # TODO: price: float  # noqa: FIX002
    """Price in Canadian dollars (CAD)."""


class FerrySchedule(BaseModel):
    date: datetime
    origin: LocationId
    destination: LocationId
    sailings: Iterable[FerrySailing]
    url: str


ScheduleGetter = Callable[[LocationId, LocationId, datetime], FerrySchedule | None]


class ScheduleDB:
    def __init__(
        self,
        *,
        ferry_connections: Iterable[FerryConnection],
        cache_dir: Path = Path("data/schedule_cache"),
        cache_ahead_days: int = 3,
    ) -> None:
        self.ferry_connections = ferry_connections
        self.cache_dir = cache_dir
        self.cache_ahead_days = cache_ahead_days
        self.refresh_interval = 60 * 60 * 24
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self.cache = {}
        self.cache_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    def _get_filepath(self, origin: LocationId, destination: LocationId, date: datetime) -> Path:
        return self.cache_dir / f"{origin}-{destination}" / f"{date.date()}.json"

    def get(self, origin: LocationId, destination: LocationId, date: datetime) -> FerrySchedule | None:
        filepath = self._get_filepath(origin, destination, date)
        schedule = self.cache.get(filepath, None)
        if schedule:
            return schedule
        if filepath.exists():
            schedule = FerrySchedule.model_validate_json(filepath.read_text(encoding="utf-8"))
            self.cache[filepath] = schedule
            return schedule
        schedule = self.download_schedule(origin, destination, date)
        if schedule:
            self.put(schedule)
        return schedule

    def put(self, schedule: FerrySchedule) -> None:
        filepath = self._get_filepath(schedule.origin, schedule.destination, schedule.date)
        self.cache[filepath] = schedule
        dirpath = filepath.parent
        if not dirpath.exists():
            dirpath.mkdir(mode=0o755, parents=True, exist_ok=True)
        filepath.write_text(schedule.model_dump_json(indent=4), encoding="utf-8")

    def download_schedule(self, origin: LocationId, destination: LocationId, date: datetime) -> FerrySchedule | None:
        route = f"{origin}-{destination}"
        url = (
            f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        )
        print(f"[{self.__class__.__name__}:INFO] fetching schedule: {route}:{date.date()}")
        try:
            response = httpx.get(url)
        except httpx.ConnectTimeout as exc:
            print(
                f"[{self.__class__.__name__}:ERROR] failed to download schedule: {route}:{date.date()}\n{exc!r}",
            )
            return None
        if response.status_code in (404, 500):
            print(f"[{self.__class__.__name__}:ERROR] schedule not found: {route}:{date.date()}")
            return None
        doc = response.text.replace("\u2060", "")
        print(f"[{self.__class__.__name__}:INFO] fetched schedule: {route}:{date.date()}")
        sailings = parse_schedule_html(html=doc, date=date)
        return FerrySchedule(
            date=date,
            origin=origin,
            destination=destination,
            sailings=sailings,
            url=url,
        )

    async def download_schedule_async(
        self,
        origin: LocationId,
        destination: LocationId,
        date: datetime,
        *,
        client: httpx.AsyncClient,
    ) -> FerrySchedule | None:
        route = f"{origin}-{destination}"
        url = (
            f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        )
        print(f"[{self.__class__.__name__}:INFO] fetching schedule: {route}:{date.date()}")
        try:
            response = await client.get(url)
        except httpx.HTTPError as exc:
            print(
                f"[{self.__class__.__name__}:ERROR] failed to download schedule: {route}:{date.date()}\n{exc!r}",
            )
            return None
        if response.status_code in (404, 500):
            print(f"[{self.__class__.__name__}:ERROR] schedule not found: {route}:{date.date()}")
            return None
        doc = response.text.replace("\u2060", "")
        print(f"[{self.__class__.__name__}:INFO] fetched schedule: {route}:{date.date()}")
        sailings = parse_schedule_html(html=doc, date=date)
        return FerrySchedule(
            date=date,
            origin=origin,
            destination=destination,
            sailings=sailings,
            url=url,
        )

    async def _download_and_save_schedule(
        self,
        connection: Connection[Terminal, Terminal],
        date: datetime,
        *,
        client: httpx.AsyncClient,
    ) -> bool:
        schedule = await self.download_schedule_async(
            origin=connection.origin.id,
            destination=connection.destination.id,
            date=date,
            client=client,
        )
        if schedule is not None:
            self.put(schedule)
            return True
        return False

    async def refresh_cache(self) -> None:
        current_date = datetime.now().date()
        current_date = datetime(current_date.year, current_date.month, current_date.day)
        dates = [current_date + timedelta(days=i) for i in range(self.cache_ahead_days)]
        for subdir, _, filenames in os.walk(self.cache_dir):
            for filename in filenames:
                date = datetime.fromisoformat(".".join(filename.split(".")[:-1]))
                if date not in dates:
                    (Path(subdir) / filename).unlink(missing_ok=True)
        # clear memory cache
        self.cache = {}
        # download new schedules
        tasks = []
        timeout = httpx.Timeout(5.0, pool=None)
        limits = httpx.Limits(max_connections=10)
        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
            for connection in self.ferry_connections:
                for date in dates:
                    filepath = self._get_filepath(connection.origin.id, connection.destination.id, date)
                    if not filepath.exists():
                        tasks.append(
                            asyncio.ensure_future(
                                self._download_and_save_schedule(
                                    connection,
                                    date,
                                    client=client,
                                ),
                            ),
                        )
            downloaded_schedules = sum(await asyncio.gather(*tasks))
        print(
            f"[{self.__class__.__name__}:INFO] finished refreshing cache, "
            f"downloaded {downloaded_schedules} schedules",
        )

    def start_refresh_thread(self) -> None:
        self._refresh_thread.start()

    def _refresh_task(self) -> None:
        while True:
            asyncio.run(self.refresh_cache())
            time.sleep(self.refresh_interval)


def parse_schedule_html(*, html: str, date: datetime) -> Iterator[FerrySailing]:
    soup = BeautifulSoup(markup=html, features="html.parser")
    table = soup.find("table", id="dailyScheduleTableOnward")
    if not table or not isinstance(table, Tag) or not table.tbody:
        return
    sailing_row_min_td_count = 3
    for row in table.tbody.find_all("tr"):
        tds = row.find_all("td")
        if len(tds) < sailing_row_min_td_count:
            continue
        departure = datetime.strptime(
            row.find_all("td")[1].text,
            "%I:%M %p",
        ).replace(year=date.year, month=date.month, day=date.day)
        arrival = datetime.strptime(
            row.find_all("td")[2].text,
            "%I:%M %p",
        ).replace(year=date.year, month=date.month, day=date.day)
        td3 = tds[3].text.strip()
        duration = int(
            datetime_to_timedelta(
                datetime.strptime(
                    td3,
                    "%Hh %Mm",
                ),
            ).total_seconds(),
        )
        sailing = FerrySailing(
            departure=departure,
            arrival=arrival,
            duration=duration,
        )
        yield sailing
