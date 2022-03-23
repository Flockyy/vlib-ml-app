from crypt import methods
import requests
import json
from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import pycaret
import pandas as pd

#Creating flask app
app = Flask(__name__)

#Load in the pickle file
model = pickle.load(open('best_pipeline.pkl', 'rb'))

#Adding routes
@app.route("/")
def hello():
    API_KEY = '' #API_KEY
    city = request.args.get('') #fill in the city logic
    
    #call API and convert response into Pyhton dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url).json()
    
    #error is unknown city name or invalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting weather details for {city.title()}. Error message = {message}'
    return render_template('base.html')
@app.route("/predict", methods = ['POST'])
def predict():
    date = request.form['Date']
    date = pd.to_datetime(date)
    # float_features = [float(x) for x in request.form.values()]
    # features = [np.array(float_features)]
    # prediction = model.predict(features)
    
    return "Test date: " + str(date)

    # return render_template('index.html', prediction_text = "The expect number of customers is {}".format(prediction))

if __name__ == "__main__":
    app.run(debug=True)