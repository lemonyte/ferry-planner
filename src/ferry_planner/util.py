from datetime import datetime, time, timedelta


def datetime_to_timedelta(dt: datetime | time, /) -> timedelta:
    return timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
