from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px
import joblib
from flask import request, jsonify

#Load Model
pipeline_path = 'C:\\Users\\Lucky\\OneDrive\\Desktop\\FinalProject\\flaskapp\\application\\SUV_model.pk1'
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
        'year': [data['year']]
    })

    # Use the pipeline to predict the price
    prediction = pipeline.predict(car_info)

    # Convert prediction to a response
    result = {"price": prediction[0]}

    return jsonify(result)

# Other code












if __name__== "__main__":
    app.run(debug=True)