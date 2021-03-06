from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app import db

from models import User
from forms import LoginForm
from forms import RegistrationForm

# End point for main page
@app.route('/')
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
        # Populate user form the form
        user = User(username=form.username.data, email=form.email.data)
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
    return redirect(url_for('index'))

# End point for profile page
@app.route('/user/<username>')
@login_required
def user(username):
    # Get username from DB
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
