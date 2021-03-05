from app import db

"""
DataBase Models - Each of the classes here represent a DB Table
"""


class User(db.Model):
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
