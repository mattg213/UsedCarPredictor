from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px


#Create app routes
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/charts-data")
def data():
    return render_template("data-charts.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/spotify")
def spotify():
    data= pd.read_json('Cleaned_2019_2020_spotify.json')
    data_dict= data.to_dict("records")
    return render_template("spotifydata.html")

@app.route("/dataanalysis")
def dataanalysis():
    return render_template("dataanalysis.html")

if __name__== "__main__":
    app.run(debug=True)