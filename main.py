""" Running a webserver to show measurements on air quality obtained by sensors on a m5Stack"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    """ Home page (index) of site"""
    return render_template("home.html")

@app.route("/measurements")
def measurements():
    """ Measurements page of site """
    return render_template("measurements.html")

if __name__ == "__main__":
    app.run(debug=True)
