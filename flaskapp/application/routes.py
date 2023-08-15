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

@app.route("/sales-by-make")
def salesbymake():
    return render_template("sales_by_make.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/sales_by_location")
def salesbylocation():
    return render_template("sales_by_location.html")

if __name__== "__main__":
    app.run(debug=True)