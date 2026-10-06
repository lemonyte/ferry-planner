from __future__ import annotations

from datetime import date, datetime

from feeds import EVERY_DAY, HSB_TO_LNG, LOCATIONS, STOPS, TIMEZONE, make_archive

from ferry_planner.gtfs import GtfsFeed, GtfsSailing

# Tuesday.
DATE = date(2026, 10, 6)


def make_feed(**files: str) -> GtfsFeed:
    return GtfsFeed(make_archive(**files), locations=LOCATIONS, timezone=TIMEZONE)


def at(day: int, hour: int, minute: int) -> datetime:
    return datetime(2026, 10, day, hour, minute, tzinfo=TIMEZONE)


def test_sailing_between_two_locations_on_a_day_the_service_runs() -> None:
    feed = make_feed(stop_times=HSB_TO_LNG)

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]


def test_no_sailings_on_a_weekday_the_service_does_not_run() -> None:
    feed = make_feed(calendar="daily,1,0,1,1,1,1,1,20260101,20261231", stop_times=HSB_TO_LNG)

    assert feed.sailings("HSB", "LNG", DATE) == []


def test_no_sailings_outside_the_service_date_range() -> None:
    feed = make_feed(calendar="daily,1,1,1,1,1,1,1,20261007,20261231", stop_times=HSB_TO_LNG)

    assert feed.sailings("HSB", "LNG", DATE) == []


def test_no_sailings_on_a_date_removed_from_the_service() -> None:
    feed = make_feed(calendar_dates="daily,20261006,2\n", stop_times=HSB_TO_LNG)

    assert feed.sailings("HSB", "LNG", DATE) == []


def test_sailings_on_a_date_added_to_the_service() -> None:
    feed = make_feed(
        calendar="daily,0,0,0,0,0,0,0,20000101,20500101",
        calendar_dates="daily,20261006,1\n",
        stop_times=HSB_TO_LNG,
    )

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]
    assert feed.sailings("HSB", "LNG", date(2026, 10, 7)) == []


def test_sailing_past_midnight_departs_on_the_day_after_its_service_day() -> None:
    feed = make_feed(stop_times="t,25:10:00,25:10:00,1,1\nt,25:50:00,25:50:00,2,2\n")

    assert feed.sailings("HSB", "LNG", DATE)[0] == GtfsSailing(departure=at(6, 1, 10), arrival=at(6, 1, 50))


def test_sailing_past_midnight_does_not_depart_before_its_service_starts() -> None:
    feed = make_feed(
        calendar="daily,1,1,1,1,1,1,1,20261006,20261231",
        stop_times="t,25:10:00,25:10:00,1,1\nt,25:50:00,25:50:00,2,2\n",
    )

    assert feed.sailings("HSB", "LNG", DATE) == []
    assert feed.sailings("HSB", "LNG", date(2026, 10, 7)) == [
        GtfsSailing(departure=at(7, 1, 10), arrival=at(7, 1, 50)),
    ]


def test_sailing_arriving_past_midnight_arrives_on_the_next_day() -> None:
    feed = make_feed(stop_times="t,23:30:00,23:30:00,1,1\nt,24:15:00,24:15:00,2,2\n")

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 23, 30), arrival=at(7, 0, 15))]


def test_sailings_are_ordered_by_departure() -> None:
    feed = make_feed(
        trips="r,daily,late\nr,daily,early\n",
        stop_times=(
            "late,17:00:00,17:00:00,1,1\nlate,17:40:00,17:40:00,2,2\n"
            "early,07:30:00,07:30:00,1,1\nearly,08:10:00,08:10:00,2,2\n"
        ),
    )

    assert [sailing.departure for sailing in feed.sailings("HSB", "LNG", DATE)] == [at(6, 7, 30), at(6, 17, 0)]


def test_same_sailing_on_two_services_is_returned_once() -> None:
    feed = make_feed(
        calendar=f"{EVERY_DAY}\nholiday,1,1,1,1,1,1,1,20260101,20261231",
        trips="r,daily,t\nr,holiday,u\n",
        stop_times=HSB_TO_LNG + HSB_TO_LNG.replace("t,", "u,"),
    )

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]


THREE_STOPS = "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:25:00,2,2\nt,10:00:00,10:00:00,3,3\n"


def test_sailing_with_a_stop_on_the_way_runs_between_every_pair_of_its_stops() -> None:
    feed = make_feed(stop_times=THREE_STOPS)

    assert feed.sailings("HSB", "NAN", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0))]
    assert feed.sailings("LNG", "NAN", DATE) == [GtfsSailing(departure=at(6, 8, 25), arrival=at(6, 10, 0))]


def test_sailing_does_not_run_against_the_order_of_its_stops() -> None:
    feed = make_feed(stop_times=THREE_STOPS)

    assert feed.sailings("NAN", "HSB", DATE) == []


def test_stop_far_from_every_location_is_ignored() -> None:
    # The second stop is about 4 km from Langdale, the nearest location.
    feed = make_feed(
        stops=STOPS.replace("2,Langdale,49.4341,-123.4721", "2,Port Mellon,49.4000,-123.4500"),
        stop_times=HSB_TO_LNG,
    )

    assert feed.sailings("HSB", "LNG", DATE) == []


def test_feed_covers_dates_in_its_date_range() -> None:
    feed = make_feed(stop_times=HSB_TO_LNG, feed_info="Publisher,20260926,20261006")

    assert feed.covers(date(2026, 9, 26))
    assert feed.covers(DATE)


def test_feed_does_not_cover_dates_outside_its_date_range() -> None:
    feed = make_feed(stop_times=HSB_TO_LNG, feed_info="Publisher,20260926,20261006")

    assert not feed.covers(date(2026, 9, 25))
    assert not feed.covers(date(2026, 10, 7))


def test_feed_without_a_date_range_covers_every_date() -> None:
    assert make_feed(stop_times=HSB_TO_LNG).covers(DATE)
    assert make_feed(stop_times=HSB_TO_LNG, feed_info="Publisher,,").covers(DATE)


# The BC Ferries feed lists the dates that a single trip is added to or removed from
# under a service named after both the trip's service and the trip.
EXCEPTION_ONLY = "daily,0,0,0,0,0,0,0,20000101,20500101"


def test_sailing_runs_on_a_date_added_for_its_trip_only() -> None:
    feed = make_feed(
        calendar=EXCEPTION_ONLY,
        calendar_dates="dailyearly,20261006,1\n",
        trips="r,daily,early\nr,daily,late\n",
        stop_times=HSB_TO_LNG.replace("t,", "early,") + "late,17:00:00,17:00:00,1,1\nlate,17:40:00,17:40:00,2,2\n",
    )

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]


def test_sailing_does_not_run_on_a_date_removed_for_its_trip_only() -> None:
    feed = make_feed(
        calendar_dates="dailyearly,20261006,2\n",
        trips="r,daily,early\nr,daily,late\n",
        stop_times=HSB_TO_LNG.replace("t,", "early,") + "late,17:00:00,17:00:00,1,1\nlate,17:40:00,17:40:00,2,2\n",
    )

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 17, 0), arrival=at(6, 17, 40))]
