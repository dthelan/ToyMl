from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, FloatField, DecimalField
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import pandas as pd

from models import User


# Create form for file up load
class FileUploadForm(FlaskForm):
    # File select button, requires data and only takes a csv
    file = FileField(validators=[FileRequired(), FileAllowed(['csv'])])
    # Add a submit button to form
    submit = SubmitField('Submit')


# Create a form for user submitted prediction
class PredictForm(FlaskForm):
    # Define all the fields that match our expected inputs
    # This form has a combination of string, float, select and decimal inputs
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

    # Method for returning a csv from the form input
    # This will make the output the same as our other method
    def csv(self):
        csv_data = pd.DataFrame([[1, self.Name.data, self.Sex.data, self.Age.data,
                                  self.Fare.data, self.Pclass.data, self.Cabin.data,
                                  self.SibSp.data, self.Parch.data, self.Ticket.data,
                                  self.Embarked.data]],
                                columns=['PassengerId', 'Name', 'Sex', 'Age',
                                         'Fare', 'Pclass', 'Cabin',
                                         'SibSp', 'Parch', 'Ticket', 'Embarked']) \
            .to_csv(index=False)
        return csv_data


# The simplest form with just a button which will kick off a request for
# a new API key
class GenerateAPI(FlaskForm):
    submit = SubmitField('Generate new API Key')


# A form for user name and password input
class LoginForm(FlaskForm):
    # String field
    username = StringField('Username', validators=[DataRequired()])
    # Password field, hides the input while typed in browsers
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# A form for user registration
class RegistrationForm(FlaskForm):
    # User name field
    username = StringField('Username', validators=[DataRequired()])
    # Email form, uses the email validator which call "email-validator"
    # Python package
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Password field which hides user text
    password = PasswordField('Password', validators=[DataRequired()])
    # Second password field which must match the first password field
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Custom validator, checks to see if a user name already exists
    def validate_username(self, username):
        # Check the db to see if a chosen user name exists
        user = User.query.filter_by(username=username.data).first()
        # If we find a user with the same user name raise an error
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Custom validator, checks to see if the email has already been used
    # The function is same as the one above
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
