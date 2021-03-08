from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Define the app as a flask app
app = Flask(__name__)
# Import the config settings
app.config.from_object(Config)
# Add the DB to Flask App
db = SQLAlchemy(app)
# Link the App and DB for migrations
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

# Import app components
# This import need to be here as they require
# the Flask App in memory
import routes
import api
# import logging





