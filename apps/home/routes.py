from xmlrpc.client import DateTime
from apps.home import blueprint
from decouple import config
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from jinja2 import TemplateNotFound
import pickle
import pandas as pd
from datetime import date, datetime
import sys
import pickle
import requests
import numpy as np

from werkzeug.security import check_password_hash, generate_password_hash

model=pickle.load(open('model_charly/BestModel.pkl', 'rb'))

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            pass

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500
    
# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

#setting up weather api_key
def get_api_key():
    api_key = config('API')
    return api_key

def get_weather_results(city, api_key):
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

#Adding routes
@blueprint.route('/preds', methods=['POST', 'GET'])
@login_required
def preds_page():
    date = pd.to_datetime(request.form['Date'])
    time = date.date()
    difference = (pd.to_datetime(time) - pd.to_datetime(2012-12-19)).days
    season = request.form['Season']
    weather = request.form['weather']
    if request.form['day'] == 'Workday':
        workingday = 1
        holiday = 0
    else:
        workingday = 0
        holiday = 1
    
    year = date.year
    month = date.month
    day = date.day_name()
    hour = date.hour
    temp = request.form['tempre']
    windspeed = request.form['vent']
    humidity = request.form['humid']
    atemp = request.form['atemp']
    if hour >= 20 or hour <= 8:
        is_night = 1
    else:
        is_night = 0
    
    dictionary = {'season': int(season), 'holiday': holiday, 'workingday':workingday, 'weather':float(weather) , 'temp':float(temp), 'atemp':float(atemp), 'humidity':float(humidity), 'windspeed':float(windspeed), 'month':float(month), 'day':day, 'hour':int(hour), 'year':int(year), 'date':difference, 'is_night':is_night}
    variables = list(dictionary.values())
    
    df = pd.DataFrame([variables], columns=dictionary.keys())
    print(dictionary.keys())
    prediction = model.predict(df)
    # Predictions(user_id)
    print(prediction)
    return render_template('home/page-preds.html', prediction=prediction)

@blueprint.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return render_template('home/results.html')
    

@blueprint.route('/weather', methods=['POST', 'GET'])
@login_required
def weather():
    city = 'Lille' #fill in the city logic
    api_key = get_api_key()
    data = get_weather_results(city, api_key)
    today = date.today()
    day = today.strftime('%B %d, %Y')
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
    day_name = today.strftime('%A')
    temp = '{0:.1f}'.format(data['main']['temp'])
    feels_like = '{0:.2f}'.format(data['main']['feels_like'])
    weather = data['weather'][0]['main']
    print(weather)
    desc = data['weather'][0]['description'].title()
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    hr, mi = (time.hour, time.minute)
    if hr>=7 and hr<18: 
        time = 'day'
    else:
        time = 'night'
    return render_template('home/home_weather.html', weather=weather, feels_like=feels_like, temp=temp, city = city, date=day, day =day_name, desc=desc, humidity=humidity, wind=wind, time=time)

@blueprint.route('/city', methods=['POST', 'GET'])
@login_required
def city_info():
    return render_template('index.html')
