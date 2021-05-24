from flask import Flask, jsonify, session, request
from config import DevelopmentConfig as config

from .models.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    #app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')
    setup_database(app)

    @app.route('/')
    def index():
        return jsonify({"message": "Index:)"})

    # registering blueprints. Do that AFTER setup_database()
    from .views.admin import admin_bp
    app.register_blueprint(admin_bp)

    from .views.books import books_bp
    app.register_blueprint(books_bp)

    from .views.auth import auth_bp
    app.register_blueprint(auth_bp)

    # enable CORS
    app.after_request(add_cors_headers)

    return app
