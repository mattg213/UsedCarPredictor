from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px
import joblib
from flask import request, jsonify

#Load Model
model = joblib.load("SUV_model.pk1")

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


# route for model
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    data = request.json

    # Extract the required fields
    has_accidents = data['has_accidents']
    make_name = data['make_name']
    mileage = data['mileage']
    model_name = data['model_name']
    owner_count = data['owner_count']
    transmission = data['transmission']
    year = data['year']

    # Combine the fields into a feature vector
    car_info = [has_accidents, make_name, mileage, model_name, owner_count, transmission, year]

    # Preprocess the input (if needed)
    processed_info = preprocess_input(car_info)  # Define this function as per your preprocessing requirements

    # Make prediction
    prediction = model.predict([processed_info])

    # Convert prediction to a response
    result = {"price": prediction[0]}

    return jsonify(result)

def preprocess_input(car_info):
#     Implement preprocessing specific to your model
#     This could include encoding categorical variables, scaling numerical variables, etc.
#     Return the processed input as needed for the model
#    pass














if __name__== "__main__":
    app.run(debug=True)