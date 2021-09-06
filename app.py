from flask import Flask, render_template, abort
import bcferries

app = Flask(__name__)
bcferries.locations.load_data('static/locations/locations.json')


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/locations')
def x():
    pass


@app.route('/routes/<start_id>-<end_id>')
def routes(start_id, end_id):
    routes = []
    start_point = [x.id for x in bcferries.locations if x.id == start_id]
    end_point = [x.id for x in bcferries.locations if x.id == end_id]
    bcferries.find_routes(start_point, end_point, routes)
    return routes


@app.route('/schedule/route=<depart_terminal_id>-<arrive_terminal_id>&date=<path:date>')
def schedule(depart_terminal_id, arrive_terminal_id, date):
    if depart_terminal_id == arrive_terminal_id:
        abort(400)
    return bcferries.get_schedule(depart_terminal_id, arrive_terminal_id, date)


@app.route('/helloworld')
def hello():
    return render_template('helloworld.html')


@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
