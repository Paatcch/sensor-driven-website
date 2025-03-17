""" Running a webserver to show measurements on air quality obtained by sensors on a m5Stack"""
from flask import Flask, render_template, request, g, jsonify
from db_handler import MeasurementsDB

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    """ Home page (index) of site"""
    return render_template("home.html")

@app.route("/measurements")
def view_measurements():
    """ Site to show all the measurements"""
    return render_template('measurements.html', list = get_db().get_measurements())

@app.route('/updateMeasurements', methods=['GET', 'POST'])
def update_mes() -> str:
    """ Adds measurements to db or extracts information from db. Not visited by users"""
    if request.method == 'POST':
        secret_key = request.headers.get('X-secret-key', '')
        json_params = request.get_json()
        try:
            if secret_key != 'Znvm9TOxa4rsCWwgMhB43tXroMZxhU1j':
                return 'Unauthorized', 401
            try:
                print('here')
                CO2_mes = int(json_params['CO2mes'])
                print(CO2_mes)
                TVOC_mes = int(json_params['TVOCmes'])
            except ValueError:
                return 'Measurement is not a number', 422
            get_db().add_measurement(CO2_mes, TVOC_mes)
        except (KeyError, TypeError):
            return "Invalid JSON", 400
    return jsonify({'latCO2': get_db().get_latest('CO2'), 'latTVOC': get_db().get_latest('TVOC'),
                    'minCO2': get_db().get_min('CO2'), 'minTVOC': get_db().get_min('TVOC'),
                    'maxCO2': get_db().get_max('CO2'), 'maxTVOC': get_db().get_max('TVOC')
                    })

def get_db() -> MeasurementsDB:
    """ Make database connection and store in Flask app context"""
    if 'db' not in g:
        g.db = MeasurementsDB()
    return g.db

@app.teardown_appcontext
def teardown_db(_exception):
    """ Closes connection to DB properly when app gets closed"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
