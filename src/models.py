from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# DataBase Models - Each of the classes here represent a DB Table

# Class for App users
# Uses Flask_Login, Mixin for user properties
class User(UserMixin, db.Model):
    """
    Database User Table containing
    id - Unique user ID
    username - Username for user
    email - User Email
    password_hash - The hash of the users password
    """
    # Define table name in DB
    __tablename__ = 'users'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
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


# Helper function, get the user ID for Flask_login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#  Helper function for API user loader from Key
@login.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None
