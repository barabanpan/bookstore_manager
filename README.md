# Prerequisites
1. `pip install -r requirements.txt`

2. In root directory create file `.env`:
```
DEBUG=True
TESTING=True
DEVELOPMENT=True
SECRET_KEY=<secret-key>
JWT_SECRET_KEY=<jwt-secret-key>
```

# Run
1. `python wsgi.py` 
or `gunicorn --bind 0.0.0.0:5000 application:app`
