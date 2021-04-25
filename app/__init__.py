from flask import Flask, jsonify, render_template, request, session
from config import DevelopmentConfig as config

from .models.database import db, base
from .models.user import User


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
#    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')
    setup_database(app)

    @app.route('/admin_users')
    def admin_users():
        users = User.return_all()
        return render_template("admin/users.html", data=users)

    @app.route('/')
    def index():
        return render_template("index.html", welcome_user=session.get("email"))

    @app.route('/books')
    def books():
        return render_template("books.html", welcome_user=session.get("email"))

    @app.route('/sign_in', methods=['GET', 'POST'])
    def sign_in():
        if request.method == "GET":
            return render_template("sign_in/sign_in.html", welcome_user=session.get("email"))

        else:
            email = request.form.get("email")
            password = request.form.get("password")
            user = User.find_by_email(email)
            right_pass = User.verify_hash(password, user.hash_password)
            if right_pass:
                session["email"] = email
                return render_template("index.html", welcome_user=session.get("email"))
            else:
                session.pop("email", None)
                return render_template("sign_in/bad_credentials.html", welcome_user=session.get("email"))

    @app.route('/registration', methods=['GET', 'POST'])
    def registration():
        if request.method == "GET":
            return render_template("sign_up/registration.html", welcome_user=session.get("email"))

        else:
            email = request.form.get("email")
            password = request.form.get("p1")

            if User.find_by_email(email):
                return render_template("sign_up/already_exists.html", welcome_user=session.get("email"))

            new_user = User(email, User.generate_hash(password))
            new_user.save_to_db()
            session["email"] = email
            return render_template("sign_up/successful.html", welcome_user=session.get("email"))

    @app.route('/sign_out')
    def sign_out():
        session.pop("email", None)
        return render_template("index.html")

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
