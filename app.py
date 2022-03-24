from contextlib import redirect_stderr
import requests
import json
from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import pycaret
import pandas as pd
import configparser

# url_today = 'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}&units=metric'
# url_forecast = 'https://api.openweathermap.org/data/2.5/forecast/daily?q={city name}&cnt={5}&appid={}&units=metric'

#setting up weather api_key
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweather']['api']

def get_weather_results(city, api_key):
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

#Creating flask app
app = Flask(__name__)

#Load in the pickle file
model = pickle.load(open('best_pipeline.pkl', 'rb'))

#Adding routes
@app.route("/", methods = ['GET', 'POST'])
def city_info():
    
    return render_template('index.html')
    

    # return render_template('index.html', prediction_text = "The expect number of customers is {}".format(prediction))

@app.route("/weathertoday", methods=['POST', 'GET'])
def weather():
    city = request.form['city'].title() #fill in the city logic
    # date = request.form['Date']
    # date = pd.to_datetime(date)
    api_key = get_api_key()
    data = get_weather_results(city, api_key)
    temp = '{0:.2f}'.format(data['main']['temp'])
    feels_like = '{0:.2f}'.format(data['main']['feels_like'])
    weather = data['weather'][0]['main']
    print(weather)
    return render_template('results.html', weather=weather, feels_like=feels_like, temp=temp, city = city)

# @app.route("/predict")
# def predict():
    
#     # float_features = [float(x) for x in request.form.values()]
#     # features = [np.array(float_features)]
#     # prediction = model.predict(features)
    
#     # #call API and convert response into Pyhton dictionary
#     # url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
#     # response = requests.get(url).json()
    
#     # #error is unknown city name or invalid api key
#     # if response.get('cod') != 200:
#     #     message = response.get('message', '')
#     #     return f'Error getting weather details for {city}. Error message = {message}'
    
#     # #get current temperature and convert it to °C 
#     # current_temperature = response.get('main', {}).get('temp')
#     # if current_temperature:
#     #     current_temperature_celcius = round(current_temperature - 273.15, 2)   
#     #     return f'Current temperature in {city} is {current_temperature} &#8451;'
#     # else:
#     #     return f'Error getting temperature for {city}' 
#     return f'Today is {str(date)} in {city}'


if __name__ == "__main__":
    app.run(debug=True)