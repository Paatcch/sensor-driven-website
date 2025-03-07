""" Running a webserver to show measurements on air quality obtained by sensors on a m5Stack"""
from flask import Flask, render_template, request, g, redirect, url_for, json, jsonify
from db_handler import MeasurementsDB

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    """ Home page (index) of site"""
    print(json.dumps('99'))
    if request.method == 'POST':
        secret_key = request.headers.get('X-secret-key', '')
        json_params = request.get_json()
        print(request.get_json())
        print(json_params['TVOCmes'])
        print(f"secret-key: {secret_key}")
        try:
            if secret_key != 'Znvm9TOxa4rsCWwgMhB43tXroMZxhU1j':
                return 'Unauthorized', 401
            try:
                CO2_mes = int(json_params['CO2mes'])
            except ValueError:
                print('Not a number. The measurement will be Null')
                CO2_mes = None
            try:
                TVOC_mes = int(json_params['TVOCmes'])
            except ValueError:
                print('Not a number. The measurement will be Null')
                TVOC_mes = None
            get_db().add_measurement(CO2_mes, TVOC_mes)
            return redirect(url_for('home'))
        except (KeyError, TypeError):
            return "Invalid JSON", 400
    return render_template("home.html")

@app.route("/measurements")
def view_measurements():
    """ Site to show all the measurements"""
    for e in get_db().get_measurements():
        print(f"get_measurements: {e}")
    print(f"get_min CO2: {get_db().get_min('CO2')}")
    print(f"get_min TVOC: {get_db().get_min('TVOC')}")
    return render_template("measurements.html")

@app.route("/min")
def get_min():
    """ Returns the minimum value from the database"""
    return jsonify({'CO2': get_db().get_min('CO2'), 'TVOC': get_db().get_min('TVOC')})

@app.route("/max")
def get_max():
    """ Returns the maximum value from the database"""
    return jsonify({'CO2': get_db().get_max('CO2'), 'TVOC': get_db().get_max('TVOC')})

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
