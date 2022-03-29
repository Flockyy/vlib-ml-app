from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pickle

app = Flask(__name__)

#Load in the pickle file
model = pickle.load(open('App/best_pipeline.pkl', 'rb'))

app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from App import routes
from App import models