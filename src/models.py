from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import abort, jsonify

from app import app
from app import auth


# DataBase Models - Each of the classes here represent a DB Table

# Class for App users
# Uses Flask_Login, Mixin for user properties
class User(UserMixin, db.Model):
    # Define table name in DB
    __tablename__ = 'users'
    # Columns
    # id - Unique user ID
    id = db.Column(db.Integer, primary_key=True)
    # username - Username for user
    username = db.Column(db.String(64), index=True, unique=True)
    # email - User Email
    email = db.Column(db.String(120), index=True, unique=True)
    # password_hash - The hash of the users password
    password_hash = db.Column(db.String(128))
    # api_key - API Key of the user, comes from a JWT hash
    api_key = db.Column(db.String(128))

    # Info on how to print user class
    # <User Name>
    # Totally optional
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Generates a hash from user provided password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Takes a user provided string and check it against the hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Logs(db.Model):
    # Define table name in DB
    __tablename__ = 'logs'
    # id - Unique user ID
    id = db.Column(db.Integer, primary_key=True)
    # user_id - This links to the user ID in the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # path - the route trying to be reached
    path = db.Column(db.String(120), index=True)
    # method = request method POST/GET
    method = db.Column(db.String(120), index=True)
    # status - return status of request
    status = db.Column(db.String(120), index=True)
    # timestamp - time of request
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


# Custom error handler to return JSON response if supplied with
# an incorrect API Key
@app.errorhandler(401)
def handle_exception(err):
    response = {str(err).split(':')[0]:
                str(err).split(':')[1].replace('password', 'API Key')}
    return jsonify(response), 401


# Method for checking a token returns a User object
# or raise a 401 error
@auth.verify_token
def verify_token(token):
    # Get the token from the header and look it up in DB
    user = User.query.filter_by(api_key=token).first()
    # If a valid user found return user
    if user is not None:
        return user
    # If user is None or no Token raise a 401
    else:
        raise abort(401)


# Helper function, used for Web Auth
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
