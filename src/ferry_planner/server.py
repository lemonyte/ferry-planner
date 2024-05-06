from __future__ import annotations

import asyncio
from collections.abc import Mapping, Sequence
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .connection import FerryConnection
from .data import ConnectionDB, LocationDB
from .location import Location, LocationId

# The options imports must be outside the TYPE_CHECKING block
# because FastAPI/Pydantic uses the type hints at runtime for validation.
from .options import RoutePlansOptions, ScheduleOptions  # noqa: TCH001
from .route import RouteBuilder, RoutePlan, RoutePlanBuilder
from .schedule import FerrySchedule, ScheduleDB

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    schedule_cache.start_refresh_thread()
    yield


app = FastAPI(lifespan=lifespan)
ROOT_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")
templates = Jinja2Templates(directory=ROOT_DIR / "templates")
location_db = LocationDB.from_files()
connection_db = ConnectionDB.from_files(location_db=location_db)
schedule_cache = ScheduleDB(
    ferry_connections=[connection for connection in connection_db.all() if isinstance(connection, FerryConnection)],
)
route_builder = RouteBuilder(connection_db)
route_plan_builder = RoutePlanBuilder(connection_db)


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
    responses={404: {"model": Literal["Schedule not found"]}},
)
async def api_schedule(options: ScheduleOptions) -> FerrySchedule | Response:
    schedule = schedule_cache.get(options.origin, options.destination, options.date)
    if schedule is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Schedule not found")
    return schedule


@app.post("/api/routeplans", response_model=Sequence[RoutePlan])
async def api_routeplans(options: RoutePlansOptions) -> Sequence[RoutePlan]:
    origin = location_db.by_id(options.origin)
    destination = location_db.by_id(options.destination)
    routes = route_builder.find_routes(origin, destination)
    route_plans = list(
        route_plan_builder.make_route_plans(
            routes=routes,
            options=options,
            schedule_getter=schedule_cache.get,
        ),
    )
    route_plans.sort(key=lambda plan: plan.duration)
    return route_plans


@app.get("/api/update", response_model=Mapping[str, str])
async def api_update() -> Mapping[str, str]:
    process = await asyncio.create_subprocess_shell("update.sh")
    await process.wait()
    if process.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update server, err={process.returncode}",
        )
    return {"result": "Update successful"}


@app.exception_handler(404)
async def not_found_handler(request: Request, _: Exception) -> HTMLResponse:
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=status.HTTP_404_NOT_FOUND,
    )
