#Imports for forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired,Email,EqualTo

# Imports for User
from flask_login import current_user
from blogApp.models import User #to check if email and username are taken already


#For login page
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')



#For registration page
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    username = StringField('Full Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords do not match.')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    #Check if email and username are taken already
    def check_email(self, field):
    	#Get all users where email==data. If one exists, email is taken
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken.')
    def check_username(self, field):
    	#Similar check for username
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken.')




#For User updating page
class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Full Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    submit = SubmitField('Update')

    #Check if new email and username are taken already
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')








