# ruff: noqa: DTZ001, DTZ005, DTZ007
import asyncio
import itertools
import os
import time
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread
from typing import Protocol

import httpx
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

from ferry_planner.connection import FerryConnection
from ferry_planner.location import LocationId
from ferry_planner.utils import datetime_to_timedelta


class FerrySailing(BaseModel):
    departure: datetime
    arrival: datetime
    duration: int
    """Duration in seconds."""
    # TODO: price: float  # noqa: FIX002
    """Price in Canadian dollars (CAD)."""
    notes: Sequence[str] | None
    """Any notes/comments posted about this sailing"""

    def __hash__(self) -> int:
        return hash((self.departure, self.arrival, self.duration, self.notes))


class FerrySchedule(BaseModel):
    date: datetime
    origin: LocationId
    destination: LocationId
    sailings: tuple[FerrySailing, ...]
    url: str
    notes: Sequence[str] | None
    """Any notes/comments posted about this schedule"""


class ScheduleGetter(Protocol):
    def __call__(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None: ...


class HtmlParseResult:
    redirect_url: str | None = None
    sailings: Sequence[FerrySailing] | None = None
    notes: list[str] | None = None

    def add_note(self, note: str) -> None:
        if self.notes is None:
            self.notes = []
        self.notes.append(note)


class ScheduleDB:
    def __init__(  # noqa: PLR0913
        self,
        *,
        ferry_connections: Sequence[FerryConnection] | set[FerryConnection] | frozenset[FerryConnection],
        base_url: str,
        cache_dir: Path,
        cache_ahead_days: int,
        refresh_interval: int,
    ) -> None:
        self.ferry_connections = ferry_connections
        self.base_url = base_url
        self.cache_dir = cache_dir
        self.cache_ahead_days = cache_ahead_days
        self.refresh_interval = refresh_interval
        self._refresh_thread = Thread(target=self._refresh_task, daemon=True)
        self._mem_cache = {}
        self.cache_dir.mkdir(mode=0o755, parents=True, exist_ok=True)

    def _get_download_url(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> str:
        return self.base_url + f"{origin_id}-{destination_id}?&scheduleDate={date.strftime('%m/%d/%Y')}"

    def _get_filepath(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> Path:
        return self.cache_dir / f"{origin_id}-{destination_id}" / f"{date.date()}.json"

    def get(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None:
        filepath = self._get_filepath(origin_id, destination_id, date=date)
        schedule = self._mem_cache.get(filepath)
        if schedule:
            return schedule
        if filepath.exists():
            schedule = FerrySchedule.model_validate_json(filepath.read_text(encoding="utf-8"))
            self._mem_cache[filepath] = schedule
            return schedule
        schedule = self.download_schedule(origin_id, destination_id, date=date)
        if schedule:
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

    def download_schedule(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> FerrySchedule | None:
        url = self._get_download_url(origin_id, destination_id, date=date)
        route = f"{origin_id}-{destination_id}"
        print(f"[{self.__class__.__name__}:INFO] fetching schedule: {route}:{date.date()}")
        max_requests_count = 3
        requests_count = 0
        while requests_count < max_requests_count:
            requests_count += 1
            try:
                response = httpx.get(url, follow_redirects=True, timeout=30.0)
            except httpx.HTTPError as exc:
                print(
                    f"[{self.__class__.__name__}:ERROR] failed to download schedule: {route}:{date.date()}\n"
                    f"{exc!r}\n"
                    f"{url}",
                )
                return None
            if not httpx.codes.is_success(response.status_code):
                print(
                    f"[{self.__class__.__name__}:ERROR] schedule not found: {route}:{date.date()}"
                    f" status {response.status_code}",
                )
                return None
            print(f"[{self.__class__.__name__}:INFO] fetched schedule: {route}:{date.date()}")
            result = parse_schedule_html(response, date)
            if result.redirect_url:
                url = result.redirect_url
                continue
            if result.sailings is None:
                break
            return FerrySchedule(
                date=date,
                origin=origin_id,
                destination=destination_id,
                sailings=tuple(result.sailings),
                url=url,
                notes=result.notes,
            )
        print(
            f"[{self.__class__.__name__}:ERROR] failed to download schedule: {route}:{date.date()}"
            f" - too many redirects",
        )
        return None

    async def download_schedule_async(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
        client: httpx.AsyncClient,
    ) -> FerrySchedule | None:
        url = self._get_download_url(origin_id, destination_id, date=date)
        route = f"{origin_id}-{destination_id}"
        print(f"[{self.__class__.__name__}:INFO] fetching schedule: {route}:{date.date()}")
        max_requests_count = 3
        requests_count = 0
        while requests_count < max_requests_count:
            requests_count += 1
            try:
                response = await client.get(url, follow_redirects=True, timeout=30.0)
            except httpx.HTTPError as exc:
                print(
                    f"[{self.__class__.__name__}:ERROR] failed to download schedule: {route}:{date.date()}\n"
                    f"{exc!r}\n"
                    f"{url}",
                )
                return None
            if not httpx.codes.is_success(response.status_code):
                print(
                    f"[{self.__class__.__name__}:ERROR] schedule not found: {route}:{date.date()}"
                    f" status {response.status_code}",
                )
                return None
            print(f"[{self.__class__.__name__}:INFO] fetched schedule: {route}:{date.date()}")
            result = parse_schedule_html(response, date)
            if result.redirect_url:
                url = result.redirect_url
                continue
            if result.sailings is None:
                break
            return FerrySchedule(
                date=date,
                origin=origin_id,
                destination=destination_id,
                sailings=tuple(result.sailings),
                url=url,
                notes=result.notes,
            )
        print(
            f"[{self.__class__.__name__}:ERROR] failed to download schedule: {route}:{date.date()}"
            f" - too many redirects",
        )
        return None

    async def _download_and_save_schedule(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
        client: httpx.AsyncClient,
    ) -> bool:
        schedule = await self.download_schedule_async(
            origin_id,
            destination_id,
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
        self._mem_cache = {}
        # download new schedules
        tasks = []
        timeout = httpx.Timeout(30.0, pool=None)
        limits = httpx.Limits(max_connections=5)
        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
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


def parse_schedule_html(response: httpx.Response, date: datetime) -> HtmlParseResult:
    result = HtmlParseResult()
    html = response.text.replace("\u2060", "")
    soup = BeautifulSoup(markup=html, features="html.parser")
    table_tag = soup.find("table", id="dailyScheduleTableOnward")
    daterange_tag = soup.find("div", id="dateRangeModal")  # for seasonal
    rows: Sequence[Tag] | None = None
    if table_tag and isinstance(table_tag, Tag) and table_tag.tbody:
        rows = table_tag.tbody.find_all("tr")
    elif daterange_tag and isinstance(daterange_tag, Tag):
        hrefs = [a["href"] for a in daterange_tag.find_all("a")]
        index = get_seasonal_schedule_daterange_index(hrefs, date)
        if index < 0:
            pass  # date is out of range
        else:
            url = response.url.scheme + "://" + response.url.host + hrefs[index]
            if index == 0 or url == str(response.url):
                rows = get_seasonal_schedule_rows(soup, date)
            else:
                result.redirect_url = url
                return result
    result.sailings = parse_sailings_from_html_rows(rows, date)
    if result.sailings is None:
        for note in [
            "Seasonal schedules have not been posted for these dates",
            "Schedules for your selected date and route are currently unavailable",
        ]:
            if note in html:
                result.add_note(note)
                result.sailings = []
                return result
        print(f"No sailings found at {response.url}")
    return result


def parse_sailings_from_html_rows(rows: Sequence[Tag] | None, date: datetime) -> Sequence[FerrySailing] | None:
    if rows is None:
        return None
    sailing_row_min_td_count = 3
    sailings: Sequence[FerrySailing] = []
    notes = None
    for row in rows:
        tds = row.find_all("td")
        if (
            len(tds) < sailing_row_min_td_count
            or "No sailings available" in tds[1].text
            or "No passengers permitted" in tds[1].text
        ):
            continue
        td1 = tds[1].text.strip().split("\n", maxsplit=1)
        if len(td1) > 1:
            notes = parse_sailig_comment(td1[1])
            # assumiing dates are always in the first note
            if is_schedule_excluded_on_date(notes[0], date):
                continue
            notes = [n for n in notes if n]
        departure = datetime.strptime(
            td1[0].strip(),
            "%I:%M %p",
        ).replace(year=date.year, month=date.month, day=date.day)
        arrival = datetime.strptime(
            row.find_all("td")[2].text.strip(),
            "%I:%M %p",
        ).replace(year=date.year, month=date.month, day=date.day)
        td3 = tds[3].text.strip()
        td3format = "%Hh %Mm" if "h " in td3 and "m" in td3 else "%Mm" if "m" in td3 else "%Hh"
        duration = int(
            datetime_to_timedelta(
                datetime.strptime(
                    td3,
                    td3format,
                ),
            ).total_seconds(),
        )
        sailing = FerrySailing(
            departure=departure,
            arrival=arrival,
            duration=duration,
            notes=notes,
        )
        sailings.append(sailing)
    return sailings


def parse_sailig_comment(comment: str) -> list[str]:
    notes: list[str] = []
    comment = comment.strip()
    notes.append(comment)
    pos = comment.find("Note:")
    if pos > 0:
        notes.append(comment[pos:])
        comment = comment[:pos].strip()
    if comment.startswith("Last "):
        notes.append(comment)
        comment = ""
    notes[0] = comment  # replace original with truncated
    return notes


def get_seasonal_schedule_rows(soup: BeautifulSoup, date: datetime) -> Sequence[Tag] | None:
    rows: Sequence[Tag] = []
    form = soup.find("form", id="seasonalSchedulesForm")
    if not isinstance(form, Tag):
        return None
    weekday_names = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    weekday = weekday_names[date.weekday()]
    for thead in form.find_all("thead"):
        if thead.text.lower().strip().startswith(weekday):
            rows = [x for x in itertools.takewhile(lambda t: t.name != "thead", thead.next_siblings) if x.name == "tr"]
            break
    return rows


def get_seasonal_schedule_daterange_index(hrefs: Sequence[str], date: datetime) -> int:
    for i, href in enumerate(hrefs):
        dates = get_seasonal_schedule_daterange_from_url(href)
        if dates and date.date() >= dates[0].date() and date.date() <= dates[1].date():
            return i
    return -1


def get_seasonal_schedule_daterange_from_url(href: str) -> tuple[datetime, datetime] | None:
    dates = href.replace("=", "-").replace("_", "-").split("-")[-2:]
    expected_dates_count = 2
    if (len(dates)) != expected_dates_count:
        return None
    date_from = datetime.strptime(dates[0], "%Y%m%d")
    date_to = datetime.strptime(dates[1], "%Y%m%d")
    return (date_from, date_to)


def is_schedule_excluded_on_date(schedule_comment: str, date: datetime) -> bool:
    if not schedule_comment:
        return False
    schedule_comment = schedule_comment.strip()
    if schedule_comment.upper().startswith("ONLY"):
        return not match_specific_schedule_date(schedule_comment, date)
    if schedule_comment.upper().startswith(("EXCEPT", "NOT AVAILABLE")):
        return match_specific_schedule_date(schedule_comment, date)
    print("Unknown comment: " + schedule_comment)
    return False


def match_specific_schedule_date(schedule_dates: str, date: datetime) -> bool:
    months: Sequence[str] = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month: int | None = None
    schedule_dates = schedule_dates.upper()
    for c in [".", "&", " ON ", " ON:"]:
        schedule_dates = schedule_dates.replace(c, ",")
    tokens = [x.strip() for x in schedule_dates.split(",")]
    tokens = [x for x in tokens if x and x not in ["ONLY", "EXCEPT", "NOT AVAILABLE"]]
    for token in tokens:
        if token in months:
            month = months.index(token) + 1
            continue
        _date: datetime
        if token.isnumeric():
            if not month:
                print(f"Failed to parse schedule dates: No month for {token} in '{schedule_dates}")
                return False
            _date = datetime(year=date.year, month=month, day=int(token))
        else:
            dt = token.split(" ")
            expected_tokens_count = 2
            if len(dt) == expected_tokens_count and dt[0].isnumeric() and dt[1] in months:
                # 01 JAN, 02 JAN, 05 FEB, 06 FEB
                _date = datetime(year=date.year, month=months.index(dt[1]) + 1, day=int(dt[0]))
            elif len(dt) == expected_tokens_count and dt[1].isnumeric() and dt[0] in months:
                # Jan 1, 2, Feb 5 & 6
                month = months.index(dt[0]) + 1
                _date = datetime(year=date.year, month=month, day=int(dt[1]))
            else:
                print(f"Failed to parse schedule dates: Unknown word '{token}' in '{schedule_dates}")
                break
        if date.month == _date.month and date.day == _date.day:
            return True
    return False
