""" Running a webserver to show measurements on air quality obtained by sensors on a m5Stack"""
from flask import Flask, render_template, request, g, redirect, url_for
from db_handler import MeasurementsDB

app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    """ Home page (index) of site"""
    if request.method == 'POST':
        try:
            CO2_mes = int(request.form["CO2mes"])
        except ValueError:
            print('Not a number. The measurement will be Null')
            CO2_mes = None
        try:
            TVOC_mes = int(request.form["TVOCmes"])
        except ValueError:
            print('Not a number. The measurement will be Null')
            TVOC_mes = None
        get_db().add_measurement(CO2_mes, TVOC_mes)
        return redirect(url_for('home'))
    return render_template("home.html")

@app.route("/measurements")
def view_measurements():
    """ Site to show all the measurements"""
    return render_template("measurements.html")
    
def get_db() -> MeasurementsDB: #What?
    """ Make database connection and store in Flask app context"""
    db_conn = getattr(g, "_db", None)
    if db_conn is None:
        db_conn = g._db = MeasurementsDB()
    return db_conn

if __name__ == "__main__":
    app.run(debug=True)
