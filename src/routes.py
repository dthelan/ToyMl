from flask import render_template, flash, redirect, url_for, request, jsonify, abort, session
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
import jwt
import pandas as pd
import io
import requests

from app import app
from app import db


from models import User, Logs
from forms import LoginForm
from forms import RegistrationForm
from forms import GenerateAPI
from forms import PredictForm

# Logging Tracker
# Dict object used for storing the current and
# previous page.
# Updated by the before_request function
User_location = {'Current': None,
                 "Target": None}

base_url = "http://localhost:5000"


# Event Logger, get the status before a request is triggered
@app.before_request
def before_request():
    # Do not log favicon
    if request.path != '/favicon.ico':
        # Get target destination and update the location dic
        User_location.update({'Target': request.path})
        # If user is logged in get the user ID
        if current_user.is_authenticated:
            userid = current_user.id
        # For unsigned in user give id -1
        else:
            userid = -1
        # Get the timestamp now
        timestamp = datetime.utcnow()
        # Populate the DB log entry
        log = Logs(user_id=userid, timestamp=timestamp,
                   source=User_location['Current'],
                   target=User_location['Target'])
        # Add new entry to DB
        db.session.add(log)
        # Commit DB Changes
        db.session.commit()
        # Update if the target isn't an api update the current
        # page with the new location
        if request.path.split('/')[1] != 'api':
            User_location.update({'Current': request.path})


# End point for main page
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """ Displays the index page accessible at '/'
    """
    return render_template('index.html')


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


@app.route('/New_Prediction', methods=['GET', 'POST'])
@login_required
def single_predict():
    form = PredictForm()
    if form.validate_on_submit():
        data = form.csv()
        response = requests.post(url_for('prediction', _external=True),
                                 data=data, params={'api_key': current_user.api_key})
        result = pd.read_csv(io.StringIO(response.text))['Survived'][0]
        if result == 0:
            outcome = "Didn't Survive"
        elif result == 1:
            outcome = "Survived"
        return render_template('new_prediction.html', form=form, value=outcome)
    return render_template('new_prediction.html', form=form)


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


# End point of logging out of the app
@app.route('/logout')
def logout():
    # Use logout_user from flask_login to logout the user
    logout_user()
    # Direct the user to index page
    # This will then redirect to the logon page
    return redirect(url_for('login'))


# End point for profile page
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = GenerateAPI()
    # Get username from DB
    user = User.query.filter_by(username=username).first_or_404()
    print(str(user.username))
    # Regenerate API Key on subbmit
    if form.validate_on_submit():
        new_key = jwt.encode({"User": str(user.username),
                              "Time": str(datetime.utcnow())},
                             app.config['SECRET_KEY'], algorithm="HS256")
        current_user.api_key = new_key
        db.session.commit()
        return render_template('user.html', user=user, form=form)
    return render_template('user.html', user=user, form=form)
