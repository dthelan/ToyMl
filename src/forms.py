from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, FloatField, IntegerField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileRequired
import pandas as pd

from models import User


class PredictForm(FlaskForm):
    Name = StringField('Name', default="Kelly, Mr. James", validators=[DataRequired()])
    Sex = SelectField('Sex', default="male", choices=['male', 'female'])
    Age = FloatField('Age', default=34, validators=[DataRequired()])
    Fare = FloatField('Fare', default=7.8292, validators=[DataRequired()])
    Pclass = SelectField('Passenger Class', default="3", choices=['1', '2', '3'])
    Cabin = StringField('Cabin', default="330911", validators=[DataRequired()])
    SibSp = DecimalField('SibSp', default=1, validators=[DataRequired()])
    Parch = DecimalField('Parch', default=1, validators=[DataRequired()])
    Ticket = StringField('Ticket', default="330911", validators=[DataRequired()])
    Embarked = StringField('Embarked', default="Q", validators=[DataRequired()])
    submit = SubmitField('Predict')

    def csv(self):
        csv_data = pd.DataFrame([[1, self.Name.data, self.Sex.data, self.Age.data,
                                  self.Fare.data, self.Pclass.data, self.Cabin.data,
                                  self.SibSp.data, self.Parch.data, self.Ticket.data,
                                  self.Embarked.data]],
                                columns=['PassengerId', 'Name', 'Sex', 'Age',
                                         'Fare', 'Pclass', 'Cabin',
                                         'SibSp', 'Parch', 'Ticket', 'Embarked'])\
            .to_csv(index=False)
        return str.encode(csv_data)


class GenerateAPI(FlaskForm):
    submit = SubmitField('Generate new API Key')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
