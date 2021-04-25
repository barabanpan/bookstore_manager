from flask import Flask, render_template, session
from config import DevelopmentConfig as config

from .models.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    #app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')
    setup_database(app)

    @app.route('/')
    def index():
        return render_template("index.html", welcome_user=session.get("email"))

    # registering blueprints. Do that AFTER setup_database()
    from .views.admin import admin_bp
    app.register_blueprint(admin_bp)

    from .views.books import books_bp
    app.register_blueprint(books_bp)

    from .views.sign_up_sign_in import sign_up_sign_in_bp
    app.register_blueprint(sign_up_sign_in_bp)

    return app
