from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, DateTimeField, StringField
from .models import Users
from datetime import date, datetime
from wtforms.validators import DataRequired


class Login(FlaskForm):
    user_name = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

