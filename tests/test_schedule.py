from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING

import httpx
from feeds import HSB_TO_LNG, LOCATIONS, TIMEZONE, make_archive

from ferry_planner.connection import FerryConnection
from ferry_planner.location import Terminal
from ferry_planner.schedule import FerrySailing, FerrySchedule, ScheduleDB

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    import pytest

GTFS_URL = "https://gtfs.example/feed.zip"
# Tuesday.
DATE = datetime(2026, 10, 6)  # noqa: DTZ001 Dates from the API have no timezone.


def make_terminal(terminal_id: str) -> Terminal:
    latitude, longitude = LOCATIONS[terminal_id]
    return Terminal(
        id=terminal_id,
        name=terminal_id,
        region="",
        long_id="",
        info_url="",
        address="",
        coordinates=f"{latitude},{longitude}",
    )


def make_db(cache_dir: Path, handler: Callable[[httpx.Request], httpx.Response]) -> ScheduleDB:
    db = ScheduleDB(
        ferry_connections=(
            FerryConnection(id="HSB-LNG", origin=make_terminal("HSB"), destination=make_terminal("LNG")),
            FerryConnection(id="LNG-HSB", origin=make_terminal("LNG"), destination=make_terminal("HSB")),
        ),
        cache_dir=cache_dir,
        gtfs_url=GTFS_URL,
    )
    db._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return db


def serve(archive: bytes, requests: list[str] | None = None) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        if requests is not None:
            requests.append(str(request.url))
        return httpx.Response(200, content=archive)

    return handler


def get(db: ScheduleDB, origin_id: str, destination_id: str, date: datetime = DATE) -> FerrySchedule | None:
    return asyncio.run(db.get(origin_id, destination_id, date=date))


def test_schedule_has_the_sailings_from_the_feed(tmp_path: Path) -> None:
    db = make_db(tmp_path, serve(make_archive(stop_times=HSB_TO_LNG)))

    schedule = get(db, "HSB", "LNG")

    assert schedule == FerrySchedule(
        date=DATE,
        origin="HSB",
        destination="LNG",
        sailings=(
            FerrySailing(
                departure=datetime(2026, 10, 6, 7, 30, tzinfo=TIMEZONE),
                arrival=datetime(2026, 10, 6, 8, 10, tzinfo=TIMEZONE),
                duration=40 * 60,
            ),
        ),
        url="https://www.bcferries.com/routes-fares/schedules/daily/HSB-LNG?&scheduleDate=10/06/2026",
    )


def test_feed_is_downloaded_once_for_several_schedules(tmp_path: Path) -> None:
    requests: list[str] = []
    db = make_db(tmp_path, serve(make_archive(), requests))

    async def get_both() -> None:
        await asyncio.gather(db.get("HSB", "LNG", date=DATE), db.get("LNG", "HSB", date=DATE))

    asyncio.run(get_both())

    assert requests == [GTFS_URL]


def test_feed_is_downloaded_again_after_the_refresh_interval(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    requests: list[str] = []
    db = make_db(tmp_path, serve(make_archive(), requests))

    get(db, "HSB", "LNG")
    now += db.refresh_interval - 1
    get(db, "LNG", "HSB")
    assert requests == [GTFS_URL]

    now += 2
    get(db, "HSB", "LNG", datetime(2026, 10, 7))  # noqa: DTZ001
    assert requests == [GTFS_URL, GTFS_URL]


def test_schedule_without_sailings_says_so(tmp_path: Path) -> None:
    db = make_db(tmp_path, serve(make_archive(stop_times=HSB_TO_LNG)))

    schedule = get(db, "LNG", "HSB")

    assert schedule is not None
    assert schedule.sailings == ()
    assert schedule.notes == ("No sailings found",)


def test_schedule_for_a_date_the_feed_does_not_cover_says_so(tmp_path: Path) -> None:
    db = make_db(tmp_path, serve(make_archive(feed_info="Publisher,20260101,20261005")))

    schedule = get(db, "HSB", "LNG")

    assert schedule is not None
    assert schedule.sailings == ()
    assert schedule.notes == ("Seasonal schedules have not been posted for these dates",)


def test_no_schedule_when_the_feed_cannot_be_downloaded(tmp_path: Path) -> None:
    db = make_db(tmp_path, lambda _: httpx.Response(503))

    assert get(db, "HSB", "LNG") is None


def test_no_schedule_when_the_feed_is_not_a_gtfs_archive(tmp_path: Path) -> None:
    db = make_db(tmp_path, serve(b"<html>Waiting room</html>"))

    assert get(db, "HSB", "LNG") is None
