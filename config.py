# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# ?


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True  # ?
    SECRET_KEY = 'aaa'

    JWT_SECRET_KEY = 'jwt-secret-key'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # to echo queries to terminal
    #SQLALCHEMY_DATABASE_URL = \
    #    "postgres://nataliia:nat_postgres_88@localhost:5432/nataliia"

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465 #587
    #MAIL_USE_TLS = True
    MAIL_USE_SSL = True

    MAIL_USERNAME = 'nataliia.dyshko@gmail.com'
    MAIL_PASSWORD = '555678gmail'
    MAIL_DEFAULT_SENDER = 'flask@example.com'


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
