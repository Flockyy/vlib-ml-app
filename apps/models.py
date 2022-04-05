from apps import db, login_manager
import datetime
from flask_login import UserMixin
import logging as lg
from werkzeug.security import generate_password_hash
import csv

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    password_hash = db.Column(db.String(length=200), nullable=False)
    
    def __repr__(self):
        return f'{self.last_name} {self.first_name}'

    def json(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'username': self.username
        }
    
    @classmethod
    def find_by_title(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
class Predicitions(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    Datetime = db.Column(db.String(), nullable=False)
    Season = db.Column(db.String(), nullable=False)
    Weather = db.Column(db.String(), nullable=False)
    Workday = db.Column(db.Boolean(), nullable=False)
    Temperature = db.Column(db.Float(), nullable=False)
    Atemperature = db.Column(db.Float(), nullable=False)
    Humidity = db.Column(db.Float(), nullable=False)
    Windspeed = db.Column(db.Float(), nullable=False)
    
    def __repr__(self):
        return f'Prediction id: {self.id}'
    
    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'Datetime': self.Datetime,
            'Season': self.Season,
            'Weather': self.Weather,
            'Workday': self.Workday,
            'Temperature': self.Temperature,
            'Atemperature': self.Atemperature,
            'Humidity': self.Humidity,
            'Windspeed': self.Windspeed
        }
    
    @classmethod
    def find_by_user_id(cls, user_id):
        prediction_list = []
        for pred in cls.query.filter_by(user_id=user_id).all():
            prediction_list.append(pred.json())
        return prediction_list
    
    @classmethod
    def get_all_in_list_with_user_name(cls):
        pred_list = []
        for pred in cls.query.join(Users).with_entities(Users.first_name, cls.Datetime, cls.Season, cls.Weather, cls.Workday, cls.Temperature, cls.Atemperature, cls.Humidity, cls.Windspeed).all():
            pred_list.append(pred)
        return pred_list
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


