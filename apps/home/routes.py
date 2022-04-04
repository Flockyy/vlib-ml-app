from xmlrpc.client import DateTime
from apps.home import blueprint
from decouple import config
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from jinja2 import TemplateNotFound
import pandas as pd
from datetime import date, datetime
import sys

import configparser
import os
import requests
from werkzeug.security import check_password_hash, generate_password_hash


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
    # config = configparser.ConfigParser()
    # path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    # config.read(os.path.join(path, 'config.ini'))
    api_token = config('API')
    return api_token

def get_weather_results(city, api_key):
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

#Adding routes
@blueprint.route('/preds', methods=['POST', 'GET'])
@login_required
def preds_page():
    date = request.form['Date']
    date = pd.to_datetime(date)
    season = request.form['Season']
    temps = request.form['weather']
    day = request.form['day'] #work out logic for workday/holiday
    tempre = request.form['tempre']
    humid = request.form['humid']
    vent = request.form['vent']
    print(day)
    return render_template('home/page-preds.html')
    

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
    desc = data['weather'][0]['description'].title()
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    hr, mi = (time.hour, time.minute)
    if hr>=7 and hr<18: 
        time = 'day'
    else:
        time = 'night'
    return render_template('home/home_weather.html', weather=weather, feels_like=feels_like, temp=temp, city = city, date=day, day =day_name, desc=desc, humidity=humidity, wind=wind, time=time)
    