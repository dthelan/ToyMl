import os
from joblib import load

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Key for encrypt
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # DB Location, From environment or in the current dir
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    # Do not flag changes in DB to app
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RF = load('../models/' + "Basic_RF.joblib")
