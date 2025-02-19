# ruff: noqa: DTZ001, DTZ005, DTZ007
import asyncio
import itertools
import os
import time
from collections.abc import Iterable, Sequence
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

MONTHS = (
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
)
WEEKDAY_NAMES = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)
NO_SAILINGS_MESSAGES = (
    "Seasonal schedules have not been posted for these dates",
    "Schedules for your selected date and route are currently unavailable",
)


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


class HtmlParseResult:
    redirect_url: str = ""
    sailings: tuple[FerrySailing, ...] = ()
    notes: tuple[str, ...] = ()
    """Notes or comments posted about this schedule."""

    @classmethod
    def redirect(cls, redirect_url: str) -> "HtmlParseResult":
        result = HtmlParseResult()
        result.redirect_url = redirect_url
        return result

    @classmethod
    def from_sailings(cls, sailings: Iterable[FerrySailing], notes: Iterable[str]) -> "HtmlParseResult":
        result = HtmlParseResult()
        result.sailings = tuple(sailings)
        result.notes = tuple(notes)
        return result


class ScheduleDownloadError(Exception):
    def __init__(self, msg: str, /, *args: Iterable, url: str) -> None:
        self.url = url
        super().__init__(f"error downloading schedule at {url}: {msg}", *args)


class ScheduleParseError(Exception):
    def __init__(self, msg: str, /, *args: Iterable, url: str) -> None:
        self.url = url
        super().__init__(f"error parsing schedule at {url}: {msg}", *args)


class ScheduleDB:
    def __init__(
        self,
        *,
        ferry_connections: Iterable[FerryConnection] | set[FerryConnection] | frozenset[FerryConnection],
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
        timeout = httpx.Timeout(30.0, pool=None)
        limits = httpx.Limits(max_connections=5)
        self._client = httpx.AsyncClient(timeout=timeout, limits=limits, follow_redirects=True)

    def _log(self, message: str, /, *, level: str = "INFO") -> None:
        print(f"[{self.__class__.__name__}:{level}] {message}")

    def _get_download_url(
        self,
        origin_id: LocationId,
        destination_id: LocationId,
        /,
        *,
        date: datetime,
    ) -> str:
        return f"{self.base_url}{origin_id}-{destination_id}?&scheduleDate={date.strftime('%m/%d/%Y')}"

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
        if schedule:
            return schedule
        if filepath.exists():
            schedule = FerrySchedule.model_validate_json(filepath.read_text(encoding="utf-8"))
            self._mem_cache[filepath] = schedule
            return schedule
        schedule = await self.download_schedule(origin_id, destination_id, date=date)
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
        except (ScheduleDownloadError, ScheduleParseError, httpx.HTTPError) as exc:
            url = exc.request.url if isinstance(exc, httpx.HTTPError) else exc.url
            self._log(
                f"failed to download schedule: {origin_id}-{destination_id}:{date.date()}\n\t{exc!r}\n\tUrl: {url}",
                level="ERROR",
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
        self._log(f"fetching schedule: {route}:{date.date()}")
        max_redirects_count = 3
        redirects = []
        while True:
            response = await self._client.get(url)
            if not httpx.codes.is_success(response.status_code):
                msg = f"status {response.status_code}"
                raise ScheduleDownloadError(msg, url=url)
            self._log(f"fetched schedule: {route}:{date.date()}")
            result = ScheduleParser.parse_schedule_html(response, date)
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

    def start_refresh_thread(self) -> None:
        # Disabled temporarily due to causing too many issues.
        # self._refresh_thread.start()  # noqa: ERA001
        pass

    def _refresh_task(self) -> None:
        while True:
            asyncio.run(self.refresh_cache())
            time.sleep(self.refresh_interval)


class ScheduleParser:
    @staticmethod
    def _log(message: str, /, *, level: str = "INFO") -> None:
        print(f"[{ScheduleParser.__name__}:{level}] {message}")

    @staticmethod
    def parse_schedule_html(response: httpx.Response, date: datetime) -> HtmlParseResult:
        html = response.text.replace("\u2060", "")
        soup = BeautifulSoup(markup=html, features="html.parser")
        table_tag = soup.find("table", id="dailyScheduleTableOnward")
        daterange_tag = soup.find("div", id="dateRangeModal")  # for seasonal
        rows = []
        if table_tag and isinstance(table_tag, Tag) and table_tag.tbody:
            rows = table_tag.tbody.find_all("tr")
        elif daterange_tag and isinstance(daterange_tag, Tag):
            hrefs = [
                a.attrs["href"]
                for a in daterange_tag.find_all("a")
                if isinstance(a, Tag) and isinstance(a.attrs["href"], str)
            ]
            index = ScheduleParser.get_seasonal_schedule_daterange_index(hrefs, date)
            if index < 0:
                msg = f"date {date} is out of seasonal schedules range"
                raise ScheduleParseError(msg, url=str(response.url))
            url = f"{response.url.scheme}://{response.url.host}{hrefs[index]}"
            if index > 0 and url != str(response.url):
                return HtmlParseResult.redirect(url)
            rows = ScheduleParser.get_seasonal_schedule_rows(str(response.url), soup, date)
        sailings = ScheduleParser.parse_sailings_from_html_rows(rows, date)
        notes = []
        if not sailings:
            err = "No sailings found"
            for msg in NO_SAILINGS_MESSAGES:
                if msg in html:
                    err = msg
                    break
            notes.append(err)
            ScheduleParser._log(f"{err} at {response.url}", level="WARNING")
        return HtmlParseResult.from_sailings(sailings, notes)

    @staticmethod
    def parse_sailings_from_html_rows(rows: Iterable[Tag], date: datetime) -> Sequence[FerrySailing]:
        sailing_row_min_td_count = 3
        sailings = []
        for row in rows:
            tds = row.find_all("td")
            if (
                len(tds) < sailing_row_min_td_count
                or "No sailings available" in tds[1].text
                or "No passengers permitted" in tds[1].text
            ):
                continue
            td1 = tds[1].text.strip().split("\n", maxsplit=1)
            departure_time, comments = td1 if len(td1) > 1 else (td1[0], "")
            if comments:
                notes = ScheduleParser.parse_sailing_comments(comments)
                if any(ScheduleParser.is_sailing_excluded_on_date(note, date) for note in notes):
                    continue
            else:
                notes = []
            departure = datetime.strptime(
                departure_time.strip(),
                "%I:%M %p",
            ).replace(year=date.year, month=date.month, day=date.day)
            arrival = datetime.strptime(
                row.find_all("td")[2].text.strip(),
                "%I:%M %p",
            ).replace(year=date.year, month=date.month, day=date.day)
            td3 = tds[3].text.strip()
            if "h " in td3 and "m" in td3:
                td3format = "%Hh %Mm"
            elif "m" in td3:
                td3format = "%Mm"
            elif "h" in td3:
                td3format = "%Hh"
            else:
                td3format = "%H:%M"
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
                notes=tuple(notes),
            )
            sailings.append(sailing)
        return sailings

    @staticmethod
    def parse_sailing_comments(comments: str) -> list[str]:
        comments = comments.strip()
        notes = comments.splitlines()
        for i, note in enumerate(notes):
            if note.startswith("Note:"):
                notes[i] = note.lstrip("Note:").strip()
        return [note.strip() for note in notes if note]

    @staticmethod
    def get_seasonal_schedule_rows(url: str, soup: BeautifulSoup, date: datetime) -> Sequence[Tag]:
        rows = []
        form = soup.find("form", id="seasonalSchedulesForm")
        if not isinstance(form, Tag):
            msg = "'seasonalSchedulesForm' not found"
            raise ScheduleParseError(msg, url=url)
        weekday = WEEKDAY_NAMES[date.weekday()]
        for thead in form.find_all("thead"):
            if thead.get_text().lower().strip().startswith(weekday):
                rows = [
                    x
                    for x in itertools.takewhile(
                        lambda t: not isinstance(t, Tag) or t.name != "thead",
                        thead.next_siblings,
                    )
                    if isinstance(x, Tag) and x.name == "tr"
                ]
                break
        return rows

    @staticmethod
    def get_seasonal_schedule_daterange_index(hrefs: Iterable[str], date: datetime) -> int:
        for i, href in enumerate(hrefs):
            dates = ScheduleParser.get_seasonal_schedule_daterange_from_url(href)
            if dates and date.date() >= dates[0].date() and date.date() <= dates[1].date():
                return i
        return -1

    @staticmethod
    def get_seasonal_schedule_daterange_from_url(href: str) -> tuple[datetime, datetime] | None:
        dates = href.replace("=", "-").replace("_", "-").split("-")[-2:]
        expected_dates_count = 2
        if (len(dates)) != expected_dates_count:
            return None
        date_from = datetime.strptime(dates[0], "%Y%m%d")
        date_to = datetime.strptime(dates[1], "%Y%m%d")
        return (date_from, date_to)

    @staticmethod
    def is_sailing_excluded_on_date(schedule_comment: str, date: datetime) -> bool:
        if not schedule_comment:
            return False
        schedule_comment = schedule_comment.strip()
        if schedule_comment.upper() == "FOOT PASSENGERS ONLY":
            return True
        if schedule_comment.upper().startswith("ONLY"):
            return not ScheduleParser.match_specific_sailing_date(schedule_comment, date)
        if schedule_comment.upper().startswith(("EXCEPT", "NOT AVAILABLE")):
            return ScheduleParser.match_specific_sailing_date(schedule_comment, date)
        ScheduleParser._log(f"unknown sailing comment: '{schedule_comment}'", level="WARNING")
        return False

    @staticmethod
    def match_specific_sailing_date(schedule_dates: str, date: datetime) -> bool:
        month: int | None = None
        schedule_dates = schedule_dates.upper()
        for c in [".", "&", " ON ", " ON:"]:
            schedule_dates = schedule_dates.replace(c, ",")
        tokens = [x.strip() for x in schedule_dates.split(",")]
        tokens = [x for x in tokens if x and x not in ["ONLY", "EXCEPT", "NOT AVAILABLE", "FOOT PASSENGERS ONLY"]]
        for token in tokens:
            if token in MONTHS:
                month = MONTHS.index(token) + 1
                continue
            if token.isnumeric():
                if not month:
                    ScheduleParser._log(
                        f"failed to parse schedule dates: No month for '{token}' in '{schedule_dates}'",
                        level="WARNING",
                    )
                    return False
                _date = datetime(year=date.year, month=month, day=int(token))
            else:
                dt = token.split(" ")
                expected_tokens_count = 2
                if len(dt) == expected_tokens_count and dt[0].isnumeric() and dt[1] in MONTHS:
                    # 01 JAN, 02 JAN, 05 FEB, 06 FEB
                    _date = datetime(year=date.year, month=MONTHS.index(dt[1]) + 1, day=int(dt[0]))
                elif len(dt) == expected_tokens_count and dt[1].isnumeric() and dt[0] in MONTHS:
                    # Jan 1, 2, Feb 5 & 6
                    month = MONTHS.index(dt[0]) + 1
                    _date = datetime(year=date.year, month=month, day=int(dt[1]))
                else:
                    ScheduleParser._log(
                        f"failed to parse schedule dates: Unknown word '{token}' in '{schedule_dates}'",
                        level="WARNING",
                    )
                    break
            if date.month == _date.month and date.day == _date.day:
                return True
        return False
