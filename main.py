from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from bcferries import (
    find_routes,
    load_data,
    locations,
    make_route_plans,
    schedule_cache,
)
from bcferries.classes import (
    FerrySchedule,
    RoutePlan,
    RoutePlansOptions,
    ScheduleOptions,
)

if TYPE_CHECKING:
    from starlette.responses import Response

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup() -> None:
    load_data("data/data.json")
    schedule_cache._refresh_thread.start()  # noqa: SLF001


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> Response:
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/api", response_class=HTMLResponse)
async def api(request: Request) -> Response:
    return templates.TemplateResponse("api.html", {"request": request})


@app.get("/api/locations", response_model=dict[str, str])
async def api_locations() -> dict:
    return {loc.id: loc.name for loc in locations.values()}


# @app.post('/api/routes')
# async def api_routes(options: classes.RoutesOptions):
#     return find_routes(options.origin, options.destination, routes)


@app.post("/api/schedule", response_model=FerrySchedule)
async def api_schedule(options: ScheduleOptions) -> FerrySchedule | None:
    return schedule_cache.get(options.origin, options.destination, options.date)


@app.post("/api/routeplans", response_model=list[RoutePlan])
async def api_routeplans(options: RoutePlansOptions) -> list[RoutePlan]:
    routes = find_routes(options.origin, options.destination)
    route_plans = make_route_plans(routes, options)
    route_plans.sort(key=lambda plan: plan.duration)
    return route_plans


@app.get("/api/update")
async def api_update() -> dict[str, str]:
    process = await asyncio.create_subprocess_shell("update.sh")
    await process.wait()
    if process.returncode != 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update server, err={process.returncode}",
        )
    # subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True, check=True)
    return {"result": "Update successful"}


@app.exception_handler(404)
async def not_found_handler(request: Request, _: Exception) -> Response:
    return templates.TemplateResponse(
        "404.html",
        {"request": request},
        status_code=status.HTTP_404_NOT_FOUND,
    )
