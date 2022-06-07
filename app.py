import time
import json
from datetime import datetime
from flask import Flask, request, render_template, abort, jsonify

from bcferries import load_data, find_routes, make_routes_plans, get_schedule
from bcferries.bcferries import locations
from bcferries.classes import JSONEncoderEx, RoutePlanOptions

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api')
def api():
    return render_template('api.html')


@app.route('/api/routes/<start_id>-<end_id>')
def routes(start_id, end_id):
    routes = []
    find_routes(start_id, end_id, routes)
    return jsonify(routes)


@app.route('/api/locations')
def get_locations():
    response = jsonify({loc.id: loc.name for loc in locations.values()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/schedule/<string:id_from>-<string:id_to>')
def schedule(id_from, id_to, date=datetime.now()):
    if id_from == id_to:
        abort(400)
    return get_schedule(id_from, id_to, date).to_json()


@app.route('/api/routeplans')
def routeplans():
    id_from = request.args.get('from')
    id_to = request.args.get('to')
    if id_from == id_to:
        abort(400)
    date = request.args.get('date')
    opt = RoutePlanOptions()
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
    if not date or date < datetime.now():
        date = datetime.now()
    opt.start_time = date
    opt.assured_load = request.args.get('assured') == 'true'
    opt.reservation = request.args.get('reservation') == 'true'
    opt.hostled = request.args.get('hostled') == 'true'
    opt.only_closest_ferry = request.args.get('show-all') == 'false'
    opt.buffer_time_minutes = (int)(request.args.get('buff-min'))
    routes = []
    start = time.perf_counter()
    find_routes(id_from, id_to, routes)
    print(f'Generated {len(routes)} routes for {id_from}-{id_to} in {time.perf_counter() - start} s')
    start = time.perf_counter()
    plans = make_routes_plans(routes, opt)
    print(f'Generated {len(plans)} plans for {id_from}-{id_to} in {time.perf_counter() - start} s')
    plans.sort(key=lambda x: x.duration)
    return json.dumps(plans, indent=4, cls=JSONEncoderEx)


if __name__ == '__main__':
    load_data('data/data.json')
    app.run(debug=True, host='0.0.0.0')
