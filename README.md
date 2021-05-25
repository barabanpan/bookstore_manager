# Prerequisites
1. `pip install -r requirements.txt`

2. In root directory create file `config.py`:
```
import os
import datetime

sqlite_uri = os.path.abspath("app/database/database.db")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '{secred-key-here}'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT = True  # session lives after browser restart
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=2)

    JWT_SECRET_KEY = '{your-very-secret-jwt-secret-key}'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
```

# Run
1. `python wsgi.py` 
or `gunicorn --bind 0.0.0.0:5000 application:app`
