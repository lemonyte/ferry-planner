"""Export results of the Python planner for the Worker's tests to compare the TypeScript port against.

Run from the repository root with `uv run python tests/export_worker_fixtures.py`.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import httpx

from ferry_planner.config import CONFIG
from ferry_planner.connection import FerryConnection
from ferry_planner.data import ConnectionDB, LocationDB
from ferry_planner.options import RoutePlansOptions, ScheduleOptions
from ferry_planner.route import RouteBuilder, RoutePlanBuilder
from ferry_planner.schedule import ScheduleDB

FIXTURES = Path("worker/test/fixtures")
DATE = "2026-10-08"
ROUTES = (
    ("TSA", "PST"),
    ("LNG", "PVB"),
    ("HSB", "NAN"),
    ("vancouver", "victoria"),
    ("smithers", "tofino"),
    ("prince_rupert", "victoria"),
    ("100_mile_house", "MIL"),
    ("atlin", "port_moody"),
    ("hope", "TSA"),
    ("tlell", "west_vancouver"),
    ("CHM", "nimpo_lake"),
    ("NAH", "gibsons"),
    ("port_hardy", "tsawwassen"),
    ("sandspit_village", "houston"),
)
PLANS: tuple[dict[str, Any], ...] = (
    {"origin": "HSB", "destination": "NAN"},
    {"origin": "TSA", "destination": "PST"},
    {"origin": "TSA", "destination": "PLH", "show_all": True},
    {"origin": "LNG", "destination": "PVB"},
    {"origin": "CMX", "destination": "TEX", "show_all": True},
    {"origin": "vancouver", "destination": "victoria"},
    {"origin": "vancouver", "destination": "victoria", "assured": True, "buffer": 30},
    {"origin": "vancouver", "destination": "victoria", "hostled": True, "buffer": 0},
    {"origin": "nanaimo", "destination": "gibsons", "show_all": True},
    {"origin": "tlell", "destination": "west_vancouver", "show_all": True},
    {"origin": "port_hardy", "destination": "tsawwassen"},
)
SCHEDULES = (
    {"origin": "HSB", "destination": "NAN", "date": DATE},
    {"origin": "TSA", "destination": "PST", "date": DATE},
    {"origin": "PPR", "destination": "PPH", "date": DATE},
    {"origin": "HSB", "destination": "NAN", "date": "2027-06-01"},
)


def normalize(value: Any) -> Any:  # noqa: ANN401
    """Leave out what the Worker leaves out, and write whole numbers the way JSON from JavaScript does."""
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items() if v is not None and k != "from_reverse"}
    if isinstance(value, list | tuple):
        return [normalize(v) for v in value]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def digest(value: Any) -> str:  # noqa: ANN401
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def main() -> None:
    archive = (FIXTURES / "feed.zip").read_bytes()
    location_db = LocationDB.from_files(CONFIG.data.location_files)
    connection_db = ConnectionDB.from_files(CONFIG.data.connection_files, location_db=location_db)
    route_builder = RouteBuilder(connection_db)
    with tempfile.TemporaryDirectory() as cache_dir:
        schedule_db = ScheduleDB(
            ferry_connections=tuple(c for c in connection_db.all() if isinstance(c, FerryConnection)),
            cache_dir=Path(cache_dir),
        )
        schedule_db._client = httpx.AsyncClient(
            transport=httpx.MockTransport(lambda _: httpx.Response(200, content=archive)),
        )
        plan_builder = RoutePlanBuilder(connection_db=connection_db, schedule_getter=schedule_db.get)

        routes = {}
        for origin, destination in ROUTES:
            found = [
                [location.id for location in route]
                for route in route_builder.find_routes(
                    origin=location_db.by_id(origin),
                    destination=location_db.by_id(destination),
                )
            ]
            # Long lists are only kept as a digest.
            routes[f"{origin}-{destination}"] = {
                "count": len(found),
                "digest": digest(found),
                **({"routes": found} if len(found) <= 25 else {}),  # noqa: PLR2004
            }

        plans = []
        for request in PLANS:
            options = RoutePlansOptions.model_validate({"date": DATE, **request})
            found = list(
                await plan_builder.make_route_plans(
                    routes=route_builder.find_routes(
                        origin=location_db.by_id(options.origin),
                        destination=location_db.by_id(options.destination),
                    ),
                    options=options,
                ),
            )
            found.sort(key=lambda plan: plan.duration)
            response = normalize([plan.model_dump(mode="json") for plan in found])
            plans.append(
                {
                    "request": {"date": DATE, **request},
                    "count": len(response),
                    "digest": digest(response),
                    "hashes": [plan["hash"][:12] for plan in response],
                    # A few whole plans show the shape of the others.
                    **({"first": response[:3]} if request == PLANS[0] else {}),
                },
            )

        schedules = []
        for request in SCHEDULES:
            options = ScheduleOptions.model_validate(request)
            schedule = await schedule_db.get(options.origin, options.destination, date=options.date)
            assert schedule is not None
            schedules.append({"request": request, "response": normalize(schedule.model_dump(mode="json"))})

    for name, value in (("routes", routes), ("plans", plans), ("schedules", schedules)):
        path = FIXTURES / f"{name}.json"
        path.write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(name, len(value), path.stat().st_size // 1000, "KB")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
