# ruff: noqa: DTZ001, DTZ005, DTZ007
import asyncio
import os
import time
from collections.abc import Callable, Sequence
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread

import httpx
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from .connection import Connection, FerryConnection
from .data import ConnectionDB


class FerrySailing(BaseModel):
    depart_time: str
    arrive_time: str
    duration: str
    # TODO: price: float  # noqa: FIX002


class FerrySchedule(BaseModel):
    date: datetime
    origin: str
    destination: str
    sailings: Sequence[FerrySailing]
    url: str


ScheduleGetter = Callable[[str, str, datetime], FerrySchedule | None]


class ScheduleDB:
    def __init__(self, *, path: Path = Path("data/schedule_cache"), connection_db: ConnectionDB) -> None:
        self.path = path
        self.connection_db = connection_db
        self.refresh_interval = 60 * 60 * 24
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self.cache = {}
        self.path.mkdir(mode=0o755, parents=True, exist_ok=True)

    def _get_filepath(self, origin: str, destination: str, date: datetime) -> Path:
        return self.path / f"{origin}-{destination}" / f"{date.date()}.json"

    def get(self, origin: str, destination: str, date: datetime) -> FerrySchedule | None:
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

    def download_schedule(self, origin: str, destination: str, date: datetime) -> FerrySchedule | None:
        route = f"{origin}-{destination}"
        url = (
            f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        )
        print(f"fetching url: {url}")
        try:
            doc = httpx.get(url).text.replace("\u2060", "")
        except httpx.ConnectTimeout as exc:
            print(exc)
            return None
        return parse_schedule_html(origin, destination, date, url, doc)

    async def download_schedule_async(
        self,
        origin: str,
        destination: str,
        date: datetime,
        *,
        client: httpx.AsyncClient,
    ) -> FerrySchedule:
        route = f"{origin}-{destination}"
        url = (
            f"https://www.bcferries.com/routes-fares/schedules/daily/{route}?&scheduleDate={date.strftime('%m/%d/%Y')}"
        )
        print(f"[INFO] fetching schedule: {route}:{date.date()}")
        doc = (await client.get(url)).text.replace("\u2060", "")
        print(f"[INFO] fetched schedule: {route}:{date.date()}")
        return parse_schedule_html(origin, destination, date, url, doc)

    async def _download_and_save_schedule(
        self,
        connection: Connection,
        date: datetime,
        *,
        client: httpx.AsyncClient,
    ) -> None:
        try:
            schedule = await self.download_schedule_async(
                origin=connection.origin.id,
                destination=connection.destination.id,
                date=date,
                client=client,
            )
        except httpx.HTTPError as exc:
            print(
                "[ERROR] failed to download schedule: "
                f"{connection.origin.id}-{connection.destination.id}:{date.date()} {exc!r}",
            )
        else:
            self.downloaded_schedules += 1
            self.put(schedule)

    async def refresh_cache(self) -> None:
        self.downloaded_schedules = 0
        ferry_connections = (
            connection for connection in self.connection_db.all() if isinstance(connection, FerryConnection)
        )
        cache_ahead_days = 3
        current_date = datetime.now().date()
        current_date = datetime(current_date.year, current_date.month, current_date.day)
        dates = [current_date + timedelta(days=i) for i in range(cache_ahead_days)]
        for subdir, _, filenames in os.walk(self.path):
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
            for connection in ferry_connections:
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
            await asyncio.gather(*tasks)
        print(f"[INFO] finished refreshing cache, downloaded {self.downloaded_schedules} schedules")

    def start_refresh_thread(self) -> None:
        self._refresh_thread.start()

    def _refresh_task(self) -> None:
        while True:
            asyncio.run(self.refresh_cache())
            time.sleep(self.refresh_interval)


def parse_sailing_table(table: Tag) -> list[FerrySailing]:
    sailings = []
    sailing_row_min_td_count = 3
    if table and table.tbody:
        for row in table.tbody.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) < sailing_row_min_td_count:
                continue
            depart_time = datetime.strptime(
                row.find_all("td")[1].text,
                "%I:%M %p",
            ).strftime("%H:%M:%S")
            arrive_time = datetime.strptime(
                row.find_all("td")[2].text,
                "%I:%M %p",
            ).strftime("%H:%M:%S")
            td3 = tds[3].text.strip()
            duration = datetime.strptime(
                td3,
                "%Hh %Mm",
            ).strftime("%H:%M")
            sailing = FerrySailing(
                depart_time=depart_time,
                arrive_time=arrive_time,
                duration=duration,
            )
            sailings.append(sailing)
    return sailings


def parse_schedule_html(
    origin: str,
    destination: str,
    date: datetime,
    url: str,
    html: str,
) -> FerrySchedule:
    soup = BeautifulSoup(markup=html, features="html.parser")
    table = soup.find("table", id="dailyScheduleTableOnward")
    sailings = parse_sailing_table(table) if isinstance(table, Tag) else []
    return FerrySchedule(
        date=date,
        origin=origin,
        destination=destination,
        sailings=sailings,
        url=url,
    )
