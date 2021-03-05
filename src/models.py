from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

"""
DataBase Models - Each of the classes here represent a DB Table
"""

# Helper function, get the user ID for Flask_login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



"""
Class for App users
Uses Flask_Login, Mixin for user properties
"""
class User(UserMixin, db.Model):
    """
    Database User Table containing
    id - Unique user ID
    username - Username for user
    email - User Email
    password_hash - The hash of the users password
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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