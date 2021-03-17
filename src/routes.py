import io
from datetime import datetime

import jwt
import pandas as pd
import requests
from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app import db
from forms import FileUploadForm
from forms import GenerateAPI
from forms import LoginForm
from forms import PredictForm
from forms import RegistrationForm
from models import User, Logs


# Event Logger, get the status after a request is triggered
@app.after_request
# After request requires a response object
def after_request(response):
    # Do not log favicon
    if request.path != '/favicon.ico':
        # If user is logged in get user ID
        if current_user.is_authenticated:
            userid = current_user.id
        # For unsigned in user give id -1
        else:
            userid = -1
        # Get the timestamp now
        timestamp = datetime.utcnow()
        # Populate the DB log entry
        # Use request.XX to get the method and path
        # Use response.status to get the status code
        log = Logs(user_id=userid, timestamp=timestamp,
                   path=request.path, method=request.method,
                   status=response.status)
        # Add new entry to DB
        db.session.add(log)
        # Commit DB Changes
        db.session.commit()
    # Return the response object
    return response


# End point for main page
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Use the file upload form
    form = FileUploadForm()
    # If the file upload form is valid on submit
    if form.validate_on_submit():
        # Get the data from the form
        # This is important reading the stream pop's it out of mem
        data = form.file.data.stream.read()
        # Perform some error handling!!!
        # Try and load top of the csv into mem as a csv
        try:
            df_file_top = pd.read_csv(io.BytesIO(data), nrows=1)
        except IOError:
            # Flash -> Could load the csv file
            flash('Invalid CSV File')
            return redirect(url_for('index'))
        # Get the headers from the csv file
        headers = list(df_file_top.columns)
        # Sort the column names so we can check against list
        headers.sort()
        # Expected col names
        expected = ['Age', 'Cabin', 'Embarked',
                    'Fare', 'Name', 'Parch',
                    'PassengerId', 'Pclass',
                    'Sex', 'SibSp', 'Ticket']
        # Check csv against list
        if headers != expected:
            # Flash -> The csv file doesn't contain the correct columns
            flash('File does not contain the correct columns')
            # Loop back round to login page
            return redirect(url_for('index'))
        # Check the csv has at least one row
        if df_file_top.shape[0] < 1:
            # Flash -> The csv file doesn't have any rows
            flash('the csv file does not contain any rows')
            # Loop back round to login page
            return redirect(url_for('index'))
        # If we pass the error handling more to the predict step
        response = requests.post(url_for('prediction', _external=True),
                                 headers={'Authorization': 'Bearer ' + current_user.api_key},
                                 data=data)
        # Convert returned string to a csv
        result = pd.read_csv(io.StringIO(response.text)).to_csv(index=False)
        # flask file send works with either an file location or BytesIO
        # Wrap csv into a BytesIO Object
        # Define a BytesIO Object
        mem = io.BytesIO()
        # Add the CSV file to it
        mem.write(result.encode())
        # Change position in buffer back to beginning
        mem.seek(0)
        # Flask send buffer to client
        return send_file(mem, as_attachment=True,
                         attachment_filename='predictions.csv',
                         mimetype='text/csv')
    # Render the index page with Flask file upload form
    return render_template('index.html', form=form)


# End point for prediction form page
@app.route('/New_Prediction', methods=['GET', 'POST'])
@login_required
def single_predict():
    # Use the Prediction form for the page
    form = PredictForm()
    # If form valid on submit
    if form.validate_on_submit():
        # Use form method to turn get the form as a csv
        data = form.csv()
        # Send the csv/form file to the prediction end point
        response = requests.post(url_for('prediction', _external=True),
                                 headers={'Authorization': 'Bearer ' + current_user.api_key},
                                 data=data)
        # Parse the results and get the outcome of the prediction of the survived column
        result = pd.read_csv(io.StringIO(response.text))['Survived'][0]
        # Translate the model prediction into plain text
        if result == 0:
            outcome = "Didn't Survive"
        else:
            outcome = "Survived"
        # Render the page with the prediction outcome included
        return render_template('new_prediction.html', form=form, value=outcome)
    # Render the page with the prediction form
    return render_template('new_prediction.html', form=form)


# Creates an endpoint for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Prevent a logged in user from going to login page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Define form to use on page
    form = LoginForm()
    # If the form is valid
    if form.validate_on_submit():
        # See if there is a valid user name for submitted info
        user = User.query.filter_by(username=form.username.data).first()
        # If no user or incorrect password
        if user is None or not user.check_password(form.password.data):
            # Flash -> Pop up for invalid password or user
            flash('Invalid username or password')
            # Loop back round to login page
            return redirect(url_for('login'))
        # If all checks pass register the user as logged on
        # uses login_user from flask_login
        login_user(user, remember=form.remember_me.data)
        # Redirect now logged in user to the index page
        return redirect(url_for('index'))
    # Render the login page for new users
    return render_template('login.html', title='Sign In', form=form)


# End point for registering
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Prevent logged user from going to the register page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Use the register form
    form = RegistrationForm()
    # If the form is valid on submit
    if form.validate_on_submit():
        # Generate a unique api_key
        api_key = jwt.encode({"User": str(form.username.data),
                              "Time": str(datetime.utcnow())},
                             app.config['SECRET_KEY'], algorithm="HS256")
        # Populate user form the form
        user = User(username=form.username.data,
                    email=form.email.data,
                    api_key=api_key)
        # Set the password hash from the password provided
        user.set_password(form.password.data)
        # Add new user to DB
        db.session.add(user)
        # Commit changes to DB
        db.session.commit()
        # Show a successful logon message
        flash('Congratulations, you are now a registered user!')
        # Redirect back to login
        return redirect(url_for('login'))
    # Display the register page with the correct form
    return render_template('register.html', title='Register', form=form)


# End point for profile page
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = GenerateAPI()
    # Get the details for the current logged in user
    user = current_user
    # If form valid on submit
    if form.validate_on_submit():
        # Generate a new api for the current user
        new_key = jwt.encode({"User": str(user.username),
                              "Time": str(datetime.utcnow())},
                             app.config['SECRET_KEY'], algorithm="HS256")
        # Change update the current user if the new api key
        current_user.api_key = new_key
        # Commit new api key to the database
        db.session.commit()
        # Render the user page with the new api key
        return render_template('user.html', user=user, form=form)
    # Render the user page with the current user details
    return render_template('user.html', user=user, form=form)


# End point of logging out of the app
@app.route('/logout')
def logout():
    # Use logout_user from flask_login to logout the user
    logout_user()
    # Direct the user to index page
    # This will then redirect to the logon page
    return redirect(url_for('login'))
