from contextlib import redirect_stderr
import requests
import json
from flask import Flask, render_template, request,jsonify, url_for, flash, redirect
import numpy as np
import pycaret
import pandas as pd
import configparser
from App import db, app
from .models import Users, Predicitions
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, current_user
import os
# url_today = 'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}&units=metric'
# url_forecast = 'https://api.openweathermap.org/data/2.5/forecast/daily?q={city name}&cnt={7}&appid={}&units=metric'

#setting up weather api_key
def get_api_key():
    config = configparser.ConfigParser()
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    config.read(os.path.join(path, 'config.ini'))
    return config['openweather']['api']

def get_weather_results(city, api_key):
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

#Adding routes
@app.route('/home')
@app.route('/')
def home_page():
    city = 'Lille' #fill in the city logic
    # date = request.form['Date']
    # date = pd.to_datetime(date)
    api_key = get_api_key()
    data = get_weather_results(city, api_key)
    temp = '{0:.2f}'.format(data['main']['temp'])
    feels_like = '{0:.2f}'.format(data['main']['feels_like'])
    weather = data['weather'][0]['main']
    print(weather)
    return render_template('home.html', weather=weather, feels_like=feels_like, temp=temp, city = city)
    


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    name = request.form['username']
    password = request.form['password']
    
    user = Users.query.filter_by(username=name).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        flash(
            f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}", category="success")
        return redirect(url_for('weather'))
    else:
        flash('Username ou mot de passe invalide', category="danger")
        return render_template('login.html')

@app.route("/home", methods = ['GET', 'POST'])
@login_required
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

    
    