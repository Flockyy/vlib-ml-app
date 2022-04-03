from apps.home import blueprint
from decouple import config
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from jinja2 import TemplateNotFound

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
    api_key = config('API')
    return api_key

def get_weather_results(city, api_key):
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

#Adding routes
@blueprint.route('/preds')
@login_required
def preds_page():
    city = 'Lille' #fill in the city logic
    # date = request.form['Date']
    # dat = pd.to_datetime(date)
    api_key = get_api_key()
    data = get_weather_results(city, api_key)
    temp = '{0:.2f}'.format(data['main']['temp'])
    feels_like = '{0:.2f}'.format(data['main']['feels_like'])
    weather = data['weather'][0]['main']
    print(city)
    return render_template('home/page-preds.html', weather=weather, feels_like=feels_like, temp=temp, city = city)
    

# @blueprint.route('/login', methods=['POST', 'GET'])
# def login_page():
#     name = request.form['username']
#     password = request.form['password']
    
#     user = Users.query.filter_by(username=name).first()
#     if user and check_password_hash(user.password_hash, password):
#         login_user(user)
#         flash(
#             f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}", category="success")
#         return redirect(url_for('weather'))
#     else:
#         flash('Username ou mot de passe invalide', category="danger")
#         return render_template('login.html')

@blueprint.route('/weather', methods=['POST', 'GET'])
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
    # return render_template('index.html', prediction_text = "The expect number of customers is {}".format(prediction))

@blueprint.route('/city', methods=['POST', 'GET'])
@login_required
def city_info():
    return render_template('index.html')

# @blueprint.route('/predict')
# def predict():
    
#     float_features = [float(x) for x in request.form.values()]
#     features = [np.array(float_features)]
#     prediction = model.predict(features)
    
#     #call API and convert response into Pyhton dictionary
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
#     response = requests.get(url).json()
    
#     #error is unknown city name or invalid api key
#     if response.get('cod') != 200:
#         message = response.get('message', '')
#         return f'Error getting weather details for {city}. Error message = {message}'
    
#     #get current temperature and convert it to °C 
#     current_temperature = response.get('main', {}).get('temp')
#     if current_temperature:
#         current_temperature_celcius = round(current_temperature - 273.15, 2)   
#         return f'Current temperature in {city} is {current_temperature} &#8451;'
#     else:
#         return f'Error getting temperature for {city}' 
#     return f'Today is {str(date)} in {city}'