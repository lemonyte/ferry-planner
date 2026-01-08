from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ferry_planner.config import CONFIG
from ferry_planner.connection import FerryConnection
from ferry_planner.data import ConnectionDB, LocationDB

# The options and db imports must be outside the TYPE_CHECKING block
# because FastAPI/Pydantic uses the type hints at runtime for validation.
from ferry_planner.db import BaseDB  # noqa: TC001
from ferry_planner.location import Location, LocationId
from ferry_planner.options import RoutePlansOptions, ScheduleOptions  # noqa: TC001
from ferry_planner.route import RouteBuilder, RoutePlan, RoutePlanBuilder
from ferry_planner.schedule import FerrySchedule

if TYPE_CHECKING:
    from js import Env

logging.basicConfig(level=CONFIG.log_level)
# Disable info logs from httpx.
logging.getLogger("httpx").setLevel(logging.WARNING)
ROOT_DIR = Path(__file__).parent
location_db = LocationDB.from_files(CONFIG.data.location_files)
connection_db = ConnectionDB.from_files(CONFIG.data.connection_files, location_db=location_db)
route_builder = RouteBuilder(connection_db)
app = FastAPI()
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")
templates = Jinja2Templates(directory=ROOT_DIR / "templates")


class ScheduleDatabaseDependency:
    """Provides a singleton schedule database instance, cached after first creation."""

    def __init__(self) -> None:
        self._db: BaseDB | None = None

    def __call__(self, request: Request) -> BaseDB:
        if self._db is None:
            env: Env = request.scope["env"]
            self._db = CONFIG.schedules.db_cls(
                ferry_connections=tuple(
                    connection for connection in connection_db.all() if isinstance(connection, FerryConnection)
                ),
                base_url=CONFIG.schedules.base_url,
                cache_ahead_days=CONFIG.schedules.cache_ahead_days,
                refresh_interval=CONFIG.schedules.refresh_interval_seconds,
                cache_dir=CONFIG.schedules.cache_dir,
                d1_instance=env.DB,
            )
            self._db.start_refresh_task()
        return self._db


db_provider = ScheduleDatabaseDependency()


class RoutePlanBuilderDependency:
    """Provides a singleton RoutePlanBuilder instance, cached after first creation."""

    def __init__(self) -> None:
        self._builder: RoutePlanBuilder | None = None

    def __call__(self, db: Annotated[BaseDB, Depends(db_provider)]) -> RoutePlanBuilder:
        if self._builder is None:
            self._builder = RoutePlanBuilder(
                connection_db=connection_db,
                schedule_getter=db.get,
            )
        return self._builder


route_plan_builder_provider = RoutePlanBuilderDependency()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/api", response_class=HTMLResponse)
async def api(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("api.html", {"request": request})


@app.get("/api/locations", response_model=Mapping[LocationId, Location])
async def api_locations() -> Mapping[LocationId, Location]:
    return location_db.dict()


@app.post(
    "/api/ferry_schedule",
    response_model=FerrySchedule,
    responses={404: {"model": Mapping[Literal["detail"], str]}},
)
async def api_schedule(
    options: ScheduleOptions,
    db: Annotated[BaseDB, Depends(db_provider)],
) -> FerrySchedule | Response:
    schedule = await db.get(options.origin, options.destination, date=options.date)
    if schedule is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Schedule not found"})
    return schedule


@app.post("/api/routeplans", response_model=Sequence[RoutePlan])
async def api_routeplans(
    options: RoutePlansOptions,
    builder: Annotated[RoutePlanBuilder, Depends(route_plan_builder_provider)],
) -> Sequence[RoutePlan]:
    origin = location_db.by_id(options.origin)
    destination = location_db.by_id(options.destination)
    routes = route_builder.find_routes(origin=origin, destination=destination)
    route_plans = list(
        await builder.make_route_plans(
            routes=routes,
            options=options,
        ),
    )
    route_plans.sort(key=lambda plan: plan.duration)
    return route_plans


@app.exception_handler(404)
async def not_found_handler(request: Request, _: Exception) -> HTMLResponse:
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=status.HTTP_404_NOT_FOUND,
    )
