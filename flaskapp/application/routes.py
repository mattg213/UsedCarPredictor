from application import app
from flask import render_template, url_for
import pandas as pd
# import json
import plotly
import numpy as np
import plotly.express as px
import joblib
from flask import request, jsonify

#Load Model
pipeline_path = './SUV_model.pk1'
pipeline = joblib.load(pipeline_path)


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


#route for model

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    data = request.json

    # Create a DataFrame with the incoming data
    car_info = pd.DataFrame({
        'has_accidents': [data['has_accidents']],
        'make_name': [data['make_name']],
        'mileage': [data['mileage']],
        'model_name': [data['model_name']],
        'owner_count': [data['owner_count']],
        'transmission': [data['transmission']],
        'year': [data['year']],
        'daysonmarket' : np.NaN,
        'dealer_zip' : np.NaN,
        'engine_displacement' : np.NaN,
        'horsepower' : np.NaN,
        'latitude' : np.NaN,
        'longitude' : np.NaN,
        'seller_rating' : np.NaN,
        'body_type' : 'SUV / Crossover',
        'fuel_type' : np.NaN,
        'maximum_seating' : np.NaN,
        'wheel_system' : np.NaN,
        'wheel_system_display' : np.NaN
    })

    # Use the pipeline to predict the price
    prediction = pipeline.predict(car_info)
    
    formatted = "%.2f"%prediction[0]
    
    formatted = round(float(formatted) / 500.0) * 500.0
    
    money_format = '${:,.2f}'.format(formatted)

    # Convert prediction to a response
    result = {"price": money_format}

    return jsonify(result)














if __name__== "__main__":
    app.run(debug=True)