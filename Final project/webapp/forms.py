from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FloatField,SubmitField,DateField,PasswordField, BooleanField
from wtforms.validators import DataRequired , Length , Email , EqualTo,ValidationError
from flask_login import current_user

from webapp.models import User


class Running_Index(FlaskForm):
    Date=DateField("Date  (Month/Day/Year)",format='%m/%d/%Y')
    Duration=FloatField("Duration (min)")
    Distance=FloatField("Distance (meters)")
    Heart_rate=IntegerField("Average Heart Rate (bpm)")
    elevation_up=IntegerField("Elevation up (meters)")
    elevation_down=IntegerField("Elevation down (meters)")
    submit=SubmitField("Calculate")

class RegistrationForm(FlaskForm):
   
    username= StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email= StringField('Email',validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Sign up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("That username is taken")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("That email is already used")
        
class LoginForm(FlaskForm):
    
    email= StringField('Email',validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('remember me')
    submit= SubmitField('Log in')



class AccountForm(FlaskForm):
   
    username= StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email= StringField('Email',validators=[DataRequired(),Email()])
    resting_heart=IntegerField('Resting heart rate',validators=[DataRequired()])
    maximum_heart=IntegerField('Maximum heart rate',validators=[DataRequired()])
    lactate_heart=IntegerField('Lactate threshold',validators=[DataRequired()])
    #password= PasswordField('Password',validators=[DataRequired()])
    #confirm_password= PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Update')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()

    # i added the user!=current_user cause without it user could only update both username and email at the same time
    # cause updating only one caused the program to raise an error about the other
        if user and user!=current_user:
            raise ValidationError("That username is taken")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()

        if user and user!=current_user:
            raise ValidationError("That email is already used")


class Import_file_csv(FlaskForm):
    
    file_path= StringField('csv file path')
    submit= SubmitField('Upload')

class Personalized_program(FlaskForm):
    generate_week=SubmitField('Generate next week')