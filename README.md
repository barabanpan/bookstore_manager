#Prerequisites
1. `pip install -r requirements.txt`

2. In root directory create file `config.py`:
```
import os
sqlite_uri = os.path.abspath("app/database/database.db")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '{secred-key-here}'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
```

#Run
1. `python wsgi.py`