import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPTokenAuth
from flask_socketio import SocketIO, emit



# Define app as a flask app
app = Flask(__name__)

# Import the config settings
app.config.from_object(Config)
# Add the DB to Flask App
db = SQLAlchemy(app)
# Link the App and DB for migrations
migrate = Migrate(app, db)

# User Flask-Login for web auth
login = LoginManager(app)
# Redirect users to the login route if require login
login.login_view = 'login'

# Use HTTPAuth for API auth and look for token in
# the header, the token should begin bearer
auth = HTTPTokenAuth(scheme='bearer')

# Add bootstrap to app
bootstrap = Bootstrap(app)

socketio = SocketIO(app)

# Import app components
# This import need to be here as they require
# the Flask App in memory
from routes import *
from api import *
from sockets import *


if __name__ == '__main__':
    socketio.run(app)