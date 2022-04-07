from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration

class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    city = StringField('City',
                      id='city_create',
                      validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    fname = StringField('Fname',
                             id='fname_create',
                             validators=[DataRequired()])
    lname = StringField('Lname',
                             id='lname_create',
                             validators=[DataRequired()])
    address = StringField('Address',
                             id='address_create',
                             validators=[DataRequired()])
    country = StringField('Country',
                             id='country_create',
                             validators=[DataRequired()])
    postcode = StringField('Postcode',
                             id='postcode_create',
                             validators=[DataRequired()])
    aboutme = StringField('Aboutme',
                             id='aboutme_create',
                             validators=[DataRequired()])

class ModifyProfileForm(FlaskForm):
    username = StringField('Username',
                        id='username_modified',
                        validators=[DataRequired()])
    email = StringField('Email',
                      id='email_modified',
                      validators=[DataRequired(), Email()])
    city = StringField('City',
                      id='city_modified',
                      validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_modified',
                             validators=[DataRequired()])
    fname = StringField('Fname',
                             id='fname_modified',
                             validators=[DataRequired()])
    lname = StringField('Lname',
                             id='lname_modified',
                             validators=[DataRequired()])
    address = StringField('Address',
                             id='address_modified',
                             validators=[DataRequired()])
    country = StringField('Country',
                             id='country_modified',
                             validators=[DataRequired()])
    postcode = StringField('Postcode',
                             id='postcode_modified',
                             validators=[DataRequired()])
    aboutme = StringField('Aboutme',
                             id='aboutme_modified',
                             validators=[DataRequired()])

