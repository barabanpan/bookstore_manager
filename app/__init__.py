from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig as config

from .models.database import db, base

jwt = JWTManager()


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def setup_jwt(app):
    jwt.init_app(app)
    from .models.revoked_token_model import RevokedTokenModel

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)


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

    # enable CORS
    app.after_request(add_cors_headers)
    setup_database(app)
    setup_jwt(app)

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

    return app
