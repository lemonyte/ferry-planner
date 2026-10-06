from __future__ import annotations

import logging
from datetime import date, datetime
from typing import TYPE_CHECKING

from feeds import EVERY_DAY, HSB_TO_LNG, LOCATIONS, STOP_TIMES_COLUMNS, STOPS, TIMEZONE, make_archive

from ferry_planner.gtfs import GtfsFeed, GtfsSailing

if TYPE_CHECKING:
    import pytest

# Tuesday.
DATE = date(2026, 10, 6)


def make_feed(**files: str) -> GtfsFeed:
    return GtfsFeed(make_archive(**files), locations=LOCATIONS, timezone=TIMEZONE)


def at(day: int, hour: int, minute: int) -> datetime:
    return datetime(2026, 10, day, hour, minute, tzinfo=TIMEZONE)


def test_sailing_between_two_locations_on_a_day_the_service_runs() -> None:
    feed = make_feed(stop_times=HSB_TO_LNG)

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]


def test_sailings_are_only_worked_out_once_for_the_same_locations_and_date(monkeypatch: pytest.MonkeyPatch) -> None:
    feed = make_feed(stop_times=HSB_TO_LNG)
    sailings = feed.sailings("HSB", "LNG", DATE)
    monkeypatch.setattr("ferry_planner.gtfs._find_journeys", None)

    assert feed.sailings("HSB", "LNG", DATE) == sailings


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

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0), stops=("LNG",)),
    ]
    assert feed.sailings("LNG", "NAN", DATE) == [GtfsSailing(departure=at(6, 8, 25), arrival=at(6, 10, 0))]


def test_sailing_does_not_run_against_the_order_of_its_stops() -> None:
    feed = make_feed(stop_times=THREE_STOPS)

    assert feed.sailings("NAN", "HSB", DATE) == []


def test_sailing_ends_at_its_first_call_at_the_destination() -> None:
    feed = make_feed(
        stop_times=(
            "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:20:00,2,2\nt,09:00:00,09:10:00,1,3\nt,09:50:00,09:50:00,2,4\n"
        ),
    )

    assert feed.sailings("HSB", "LNG", DATE) == [
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10)),
        GtfsSailing(departure=at(6, 9, 10), arrival=at(6, 9, 50)),
    ]


def test_sailing_departs_at_its_last_call_at_the_origin() -> None:
    feed = make_feed(
        stop_times=(
            "t,07:30:00,07:30:00,1,1\nt,08:10:00,08:20:00,2,2\nt,09:00:00,09:10:00,1,3\nt,10:50:00,10:50:00,3,4\n"
        ),
    )

    assert feed.sailings("HSB", "NAN", DATE) == [GtfsSailing(departure=at(6, 9, 10), arrival=at(6, 10, 50))]


def test_sailing_does_not_continue_on_an_earlier_part_of_its_trip() -> None:
    feed = make_feed(
        stop_times=(
            "t,07:00:00,07:00:00,2,1\nt,08:00:00,08:10:00,3,2\nt,09:00:00,09:10:00,1,3\nt,09:50:00,09:50:00,2,4\n"
        ),
    )

    assert feed.sailings("HSB", "NAN", DATE) == []


def test_stop_far_from_every_location_is_ignored() -> None:
    # The second stop is about 1 km from Langdale, the nearest location.
    feed = make_feed(
        stops=STOPS.replace("2,Langdale,49.4341,-123.4721", "2,Langdale Heights,49.4430,-123.4720"),
        stop_times=HSB_TO_LNG,
    )

    assert feed.sailings("HSB", "LNG", DATE) == []


def test_stop_without_coordinates_is_ignored() -> None:
    feed = make_feed(stops=f"{STOPS}4,Somewhere,,\n", stop_times=HSB_TO_LNG + "t,09:00:00,09:00:00,4,3\n")

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]


def test_stop_without_times_is_passed_through() -> None:
    feed = make_feed(stop_times="t,07:30:00,07:30:00,1,1\nt,,,2,2\nt,10:00:00,10:00:00,3,3\n")

    assert feed.sailings("HSB", "NAN", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0))]


def test_stop_with_only_one_time_arrives_and_departs_at_it() -> None:
    feed = make_feed(stop_times="t,,07:30:00,1,1\nt,08:10:00,,2,2\nt,10:00:00,,3,3\n")

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]
    assert feed.sailings("LNG", "NAN", DATE) == [GtfsSailing(departure=at(6, 8, 10), arrival=at(6, 10, 0))]


def test_feed_without_a_calendar_runs_services_on_their_added_dates() -> None:
    archive = make_archive(calendar=None, calendar_dates="daily,20261006,1\n", stop_times=HSB_TO_LNG)
    feed = GtfsFeed(archive, locations=LOCATIONS, timezone=TIMEZONE)

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]
    assert feed.sailings("HSB", "LNG", date(2026, 10, 7)) == []


def test_feed_without_calendar_dates_runs_services_on_their_calendar() -> None:
    archive = make_archive(calendar_dates=None, stop_times=HSB_TO_LNG)
    feed = GtfsFeed(archive, locations=LOCATIONS, timezone=TIMEZONE)

    assert feed.sailings("HSB", "LNG", DATE) == [GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 8, 10))]


def test_locations_without_sailings_are_logged(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        make_feed(stop_times=HSB_TO_LNG)

    assert [record.getMessage() for record in caplog.records] == ["no sailings in the GTFS feed for NAN"]


PICKUP_COLUMNS = f"{STOP_TIMES_COLUMNS},pickup_type,drop_off_type"


def test_no_sailing_from_a_stop_that_cannot_be_boarded_at() -> None:
    feed = make_feed(
        stop_times_columns=PICKUP_COLUMNS,
        stop_times="t,07:30:00,07:30:00,1,1,1,0\nt,08:10:00,08:10:00,2,2,0,0\n",
    )

    assert feed.sailings("HSB", "LNG", DATE) == []


def test_no_sailing_to_a_stop_that_cannot_be_alighted_at() -> None:
    feed = make_feed(
        stop_times_columns=PICKUP_COLUMNS,
        stop_times="t,07:30:00,07:30:00,1,1,0,0\nt,08:10:00,08:10:00,2,2,0,1\n",
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


# The BC Ferries feed lists each part of a sailing that calls at several terminals as a trip of its own.
TRIPS = "r,daily,a\nr,daily,b\nr,daily,c\n"
HSB_TO_LNG_BY_8_10 = "a,07:30:00,07:30:00,1,1\na,08:10:00,08:10:00,2,2\n"
LNG_TO_NAN_AT_8_25 = "b,08:25:00,08:25:00,2,1\nb,10:00:00,10:00:00,3,2\n"


def test_sailing_continues_on_the_trip_that_departs_from_where_it_arrives() -> None:
    feed = make_feed(trips=TRIPS, stop_times=HSB_TO_LNG_BY_8_10 + LNG_TO_NAN_AT_8_25)

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0), stops=("LNG",)),
    ]


def test_sailing_continues_on_the_first_trip_to_arrive() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=HSB_TO_LNG_BY_8_10 + "c,08:15:00,08:15:00,2,1\nc,10:30:00,10:30:00,3,2\n" + LNG_TO_NAN_AT_8_25,
    )

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0), stops=("LNG",)),
    ]


def test_sailing_does_not_continue_on_a_trip_that_departs_before_it_arrives() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=HSB_TO_LNG_BY_8_10 + "b,08:05:00,08:05:00,2,1\nb,10:00:00,10:00:00,3,2\n",
    )

    assert feed.sailings("HSB", "NAN", DATE) == []


def test_sailing_does_not_continue_on_a_trip_that_departs_hours_after_it_arrives() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=HSB_TO_LNG_BY_8_10 + "b,10:15:00,10:15:00,2,1\nb,12:00:00,12:00:00,3,2\n",
    )

    assert feed.sailings("HSB", "NAN", DATE) == []


def test_sailing_continues_past_midnight() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=(
            "a,23:30:00,23:30:00,1,1\na,24:15:00,24:15:00,2,2\nb,24:30:00,24:30:00,2,1\nb,25:30:00,25:30:00,3,2\n"
        ),
    )

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 23, 30), arrival=at(7, 1, 30), stops=("LNG",)),
    ]
    assert feed.sailings("LNG", "NAN", date(2026, 10, 7)) == [
        GtfsSailing(departure=at(7, 0, 30), arrival=at(7, 1, 30)),
    ]


def test_sailing_with_a_transfer_is_left_out_when_a_later_sailing_arrives_no_later() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=HSB_TO_LNG_BY_8_10 + LNG_TO_NAN_AT_8_25 + "c,08:00:00,08:00:00,1,1\nc,09:40:00,09:40:00,3,2\n",
    )

    assert feed.sailings("HSB", "NAN", DATE) == [GtfsSailing(departure=at(6, 8, 0), arrival=at(6, 9, 40))]


def test_sailing_without_a_transfer_is_kept_when_a_later_sailing_arrives_earlier() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=HSB_TO_LNG_BY_8_10 + LNG_TO_NAN_AT_8_25 + "c,07:00:00,07:00:00,1,1\nc,11:00:00,11:00:00,3,2\n",
    )

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 7, 0), arrival=at(6, 11, 0)),
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0), stops=("LNG",)),
    ]


# Transfers at Langdale take at least 45 minutes.
LNG_TRANSFER = "2,2,2,2700\n"


def test_sailing_does_not_continue_on_a_trip_that_departs_within_the_minimum_transfer_time() -> None:
    feed = make_feed(trips=TRIPS, stop_times=HSB_TO_LNG_BY_8_10 + LNG_TO_NAN_AT_8_25, transfers=LNG_TRANSFER)

    assert feed.sailings("HSB", "NAN", DATE) == []


def test_sailing_continues_on_a_trip_that_departs_after_the_minimum_transfer_time() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times=HSB_TO_LNG_BY_8_10 + "b,08:55:00,08:55:00,2,1\nb,10:30:00,10:30:00,3,2\n",
        transfers=LNG_TRANSFER,
    )

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 30), stops=("LNG",)),
    ]


def test_sailing_stays_on_its_trip_without_waiting_for_the_minimum_transfer_time() -> None:
    feed = make_feed(stop_times=THREE_STOPS, transfers=LNG_TRANSFER)

    assert feed.sailings("HSB", "NAN", DATE) == [
        GtfsSailing(departure=at(6, 7, 30), arrival=at(6, 10, 0), stops=("LNG",)),
    ]


def test_sailing_does_not_continue_from_a_stop_that_cannot_be_alighted_at() -> None:
    feed = make_feed(
        trips=TRIPS,
        stop_times_columns=PICKUP_COLUMNS,
        stop_times="a,07:30:00,07:30:00,1,1,0,0\na,08:10:00,08:10:00,2,2,0,1\n" + LNG_TO_NAN_AT_8_25,
    )

    assert feed.sailings("HSB", "NAN", DATE) == []
