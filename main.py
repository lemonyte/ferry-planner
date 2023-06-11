import subprocess

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from bcferries import classes, find_routes, load_data, locations, make_route_plans, schedule_cache

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.on_event('startup')
async def init():
    load_data('data/data.json')
    schedule_cache._refresh_thread.start()


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})


@app.get('/api', response_class=HTMLResponse)
async def api(request: Request):
    return templates.TemplateResponse('api.html', {'request': request})


@app.get('/api/locations', response_model=dict[str, str])
async def api_locations():
    return {loc.id: loc.name for loc in locations.values()}


# @app.post('/api/routes')
# async def api_routes(options: classes.RoutesOptions):
#     return find_routes(options.origin, options.destination, routes)


@app.post('/api/schedule', response_model=classes.FerrySchedule)
async def api_schedule(options: classes.ScheduleOptions):
    return schedule_cache.get(options.origin, options.destination, options.date)


@app.post('/api/routeplans', response_model=list[classes.RoutePlan])
async def api_routeplans(options: classes.RoutePlansOptions):
    routes = find_routes(options.origin, options.destination)
    route_plans = make_route_plans(routes, options)
    route_plans.sort(key=lambda plan: plan.duration)
    return route_plans


@app.get('/api/update')
async def api_update():
    p = subprocess.run(['/bin/sh', 'update.sh'], shell=True)
    p2 = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], shell=True)
    if p.returncode == 0 and p2.returncode == 0:
        return {'result': "Update successful"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update server")


@app.exception_handler(404)
async def not_found_handler(request: Request, exception):
    return templates.TemplateResponse('404.html', {'request': request}, 404)
