from __future__ import annotations

import asyncio
from datetime import datetime
from typing import TYPE_CHECKING

import httpx
from feeds import HSB_TO_LNG, LOCATIONS, TIMEZONE, make_archive

from ferry_planner.connection import FerryConnection
from ferry_planner.location import Terminal
from ferry_planner.schedule import FEED_RETRY_SECONDS, FerrySailing, FerrySchedule, ScheduleDB

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from pathlib import Path

    import pytest

GTFS_URL = "https://gtfs.example/feed.zip"
# Tuesday.
DATE = datetime(2026, 10, 6)  # noqa: DTZ001 Dates from the API have no timezone.
NEXT_DATE = datetime(2026, 10, 7)  # noqa: DTZ001
THREE_STOPS = "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:25:00,2,2\nt,10:00:00,10:00:00,3,3\n"
BOTH_WAYS = {
    "trips": "r,daily,t\nr,daily,u\n",
    "stop_times": HSB_TO_LNG + "u,09:00:00,09:00:00,2,1\nu,09:40:00,09:40:00,1,2\n",
}


def make_terminal(terminal_id: str) -> Terminal:
    latitude, longitude = LOCATIONS[terminal_id]
    return Terminal(
        id=terminal_id,
        name=f"{terminal_id} Terminal",
        region="",
        long_id="",
        info_url="",
        address="",
        coordinates=f"{latitude},{longitude}",
    )


def make_db(cache_dir: Path, handler: Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]) -> ScheduleDB:
    db = ScheduleDB(
        ferry_connections=(
            FerryConnection(id="HSB-LNG", origin=make_terminal("HSB"), destination=make_terminal("LNG")),
            FerryConnection(id="LNG-HSB", origin=make_terminal("LNG"), destination=make_terminal("HSB")),
            FerryConnection(id="HSB-NAN", origin=make_terminal("HSB"), destination=make_terminal("NAN")),
        ),
        cache_dir=cache_dir,
        gtfs_url=GTFS_URL,
    )
    db._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return db


def serve(
    *contents: bytes | int,
    requests: list[str] | None = None,
) -> Callable[[httpx.Request], Coroutine[None, None, httpx.Response]]:
    """Respond to each request with the next of the given feed archives or error statuses, repeating the last."""
    remaining = list(contents)

    async def handler(request: httpx.Request) -> httpx.Response:
        if requests is not None:
            requests.append(str(request.url))
        # Lets the other schedules that were requested at once ask for the feed during the download.
        await asyncio.sleep(0)
        content = remaining.pop(0) if len(remaining) > 1 else remaining[0]
        return httpx.Response(content) if isinstance(content, int) else httpx.Response(200, content=content)

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
    db = make_db(tmp_path, serve(make_archive(), requests=requests))

    async def get_both() -> None:
        await asyncio.gather(db.get("HSB", "LNG", date=DATE), db.get("LNG", "HSB", date=DATE))

    asyncio.run(get_both())

    assert requests == [GTFS_URL]


def test_feed_is_downloaded_once_for_several_schedules_in_each_event_loop(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    requests: list[str] = []
    db = make_db(tmp_path, serve(make_archive(), requests=requests))

    async def get_both(date: datetime) -> None:
        await asyncio.gather(db.get("HSB", "LNG", date=date), db.get("LNG", "HSB", date=date))

    asyncio.run(get_both(DATE))
    now += db.refresh_interval + 1
    asyncio.run(get_both(NEXT_DATE))

    assert requests == [GTFS_URL, GTFS_URL]


def test_feed_is_downloaded_again_after_the_refresh_interval(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    requests: list[str] = []
    db = make_db(tmp_path, serve(make_archive(), requests=requests))

    get(db, "HSB", "LNG")
    now += db.refresh_interval - 1
    get(db, "LNG", "HSB")
    assert requests == [GTFS_URL]

    now += 2
    get(db, "HSB", "LNG", NEXT_DATE)
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
    db = make_db(tmp_path, serve(503))

    assert get(db, "HSB", "LNG") is None


def test_no_schedule_when_the_feed_is_not_a_gtfs_archive(tmp_path: Path) -> None:
    db = make_db(tmp_path, serve(b"<html>Waiting room</html>"))

    assert get(db, "HSB", "LNG") is None


def test_no_schedule_when_the_feed_is_malformed(tmp_path: Path) -> None:
    # The stop sequences are missing.
    db = make_db(tmp_path, serve(make_archive(stop_times="t,07:30:00,07:30:00,1\nt,08:10:00,08:10:00,2\n")))

    assert get(db, "HSB", "LNG") is None


def test_previous_feed_is_used_when_the_feed_cannot_be_downloaded_again(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    db = make_db(tmp_path, serve(make_archive(), 503))
    get(db, "HSB", "LNG")

    now += db.refresh_interval + 1
    schedule = get(db, "HSB", "LNG", NEXT_DATE)

    assert schedule is not None
    assert len(schedule.sailings) == 1


def test_failed_download_is_not_repeated_for_every_schedule(tmp_path: Path) -> None:
    requests: list[str] = []
    db = make_db(tmp_path, serve(503, requests=requests))

    async def get_both() -> list[FerrySchedule | None]:
        return list(await asyncio.gather(db.get("HSB", "LNG", date=DATE), db.get("LNG", "HSB", date=DATE)))

    assert asyncio.run(get_both()) == [None, None]
    assert get(db, "HSB", "LNG", NEXT_DATE) is None
    assert requests == [GTFS_URL]


def test_feed_is_downloaded_again_a_while_after_a_failed_download(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    db = make_db(tmp_path, serve(503, make_archive()))
    assert get(db, "HSB", "LNG") is None

    now += FEED_RETRY_SECONDS + 1

    assert get(db, "HSB", "LNG") is not None


def test_schedule_without_sailings_gains_those_added_to_the_feed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    db = make_db(tmp_path, serve(make_archive(), make_archive(**BOTH_WAYS)))
    get(db, "LNG", "HSB")

    now += db.refresh_interval + 1
    schedule = get(db, "LNG", "HSB")

    assert schedule is not None
    assert len(schedule.sailings) == 1
    assert schedule.notes == ()


def test_schedule_gains_sailings_once_the_feed_covers_its_date(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: now)
    db = make_db(
        tmp_path,
        serve(
            make_archive(feed_info="Publisher,20260101,20261005"),
            make_archive(feed_info="Publisher,20260101,20261231"),
        ),
    )
    get(db, "HSB", "LNG")

    now += db.refresh_interval + 1
    schedule = get(db, "HSB", "LNG")

    assert schedule is not None
    assert len(schedule.sailings) == 1


def test_schedule_without_sailings_saved_before_a_restart_is_looked_up_again(tmp_path: Path) -> None:
    make_db(tmp_path, serve(make_archive())).put(
        FerrySchedule(date=DATE, origin="HSB", destination="LNG", sailings=(), url="", notes=("No sailings found",)),
    )

    schedule = get(make_db(tmp_path, serve(make_archive())), "HSB", "LNG")

    assert schedule is not None
    assert len(schedule.sailings) == 1


def test_schedule_with_sailings_is_kept_across_a_restart(tmp_path: Path) -> None:
    saved = get(make_db(tmp_path, serve(make_archive())), "HSB", "LNG")

    assert saved is not None
    assert get(make_db(tmp_path, serve(503)), "HSB", "LNG") == saved


def test_sailing_that_calls_at_terminals_on_the_way_names_them(tmp_path: Path) -> None:
    db = make_db(tmp_path, serve(make_archive(stop_times=THREE_STOPS)))

    schedule = get(db, "HSB", "NAN")

    assert schedule is not None
    assert [sailing.notes for sailing in schedule.sailings] == [("Via LNG Terminal",)]
