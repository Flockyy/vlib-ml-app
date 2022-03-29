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
        
