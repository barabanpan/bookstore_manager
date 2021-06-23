import os
import datetime
from dotenv import dotenv_values

sqlite_uri = os.path.abspath("app/database/database.db")
project_root = os.getcwd()
env = dotenv_values(os.path.join(project_root, ".env"))


class Config(object):
    DEBUG = env['DEBUG']  # True for development, False for production
    DEVELOPMENT = env['DEVELOPMENT']  # True for development, False for production
    TESTING = env['TESTING']  # True for testing
    CSRF_ENABLED = True
    SECRET_KEY = env['SECRET_KEY']

    PERMANENT = True  # session lives after browser restart
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=2)

    JWT_SECRET_KEY = env['JWT_SECRET_KEY']
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # to echo queries to terminal
