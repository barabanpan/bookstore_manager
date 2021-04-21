from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
#    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')
    db = SQLAlchemy(app)

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/books')
    def books():
        return render_template("books.html")

    @app.route('/sign_up')
    def sign_up():
        return render_template("sign_up.html")

    @app.route('/registration')
    def registration():
        return render_template("registration.html")
        #jsonify({"message": "Hello, World!"})

#    # not happening in main because app is imported to wsgi
#    setup_database(app)
#    setup_jwt(app)

    # adding resources. Do that AFTER setup_database()
#    from .views import users_bp, add_users_routes
#    add_users_routes()  # creates it's own api and adds it there
#    app.register_blueprint(users_bp)  # blueprint connects that api and app

#    from .views import email_sender_bp, add_emails_routes
#    add_emails_routes()  # creates it's own api and adds it there
#    app.register_blueprint(email_sender_bp)  # blueprint connects that api and app

    return app