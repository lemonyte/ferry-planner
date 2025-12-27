import itertools
from collections.abc import Iterable, Sequence
from datetime import datetime
from typing import Protocol

from bs4 import BeautifulSoup, Tag
from httpx import Response
from pydantic import BaseModel

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


class ScheduleParser:
    @staticmethod
    def _log(message: str, /, *, level: str = "INFO") -> None:
        print(f"[{ScheduleParser.__name__}:{level}] {message}")

    @staticmethod
    def parse_schedule_html(response: Response, date: datetime) -> HtmlParseResult:
        html = response.text.replace("\u2060", "")
        soup = BeautifulSoup(markup=html, features="html.parser")
        table_tag = soup.find("table", id="dailyScheduleTableOnward")
        daterange_tag = soup.find("div", id="dateRangeModal")  # for seasonal
        rows = []
        if table_tag and table_tag.tbody:
            rows = table_tag.tbody.find_all("tr")
        elif daterange_tag:
            hrefs = [a.attrs["href"] for a in daterange_tag.find_all("a") if isinstance(a.attrs["href"], str)]
            try:
                index = ScheduleParser.get_seasonal_schedule_daterange_index(hrefs, date)
            except Exception as exc:
                msg = "failed to parse seasonal schedule daterange"
                raise ScheduleParseError(msg, url=str(response.url)) from exc
            if index < 0:
                msg = f"date {date} is out of seasonal schedules range"
                raise ScheduleParseError(msg, url=str(response.url))
            url = f"{response.url.scheme}://{response.url.host}{hrefs[index]}"
            if index > 0 and url != str(response.url):
                return HtmlParseResult.redirect(url)
            rows = ScheduleParser.get_seasonal_schedule_rows(str(response.url), soup, date)
        try:
            sailings = ScheduleParser.parse_sailings_from_html_rows(rows, date)
        except Exception as exc:
            msg = "failed to parse schedule from HTML rows"
            raise ScheduleParseError(msg, url=str(response.url)) from exc
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
        if form is None:
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
