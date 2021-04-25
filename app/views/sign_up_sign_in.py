from flask.blueprints import Blueprint
from flask import render_template, request, session

from app.models.user_model import UserModel

sign_up_sign_in_bp = Blueprint('sign_up_sign_in', __name__)


@sign_up_sign_in_bp.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == "GET":
        return render_template("sign_in/sign_in.html", welcome_user=session.get("email"))

    else:
        email = request.form.get("email")
        password = request.form.get("password")
        user = UserModel.find_by_email(email)
        right_pass = UserModel.verify_hash(password, user.hash_password)
        if right_pass:
            session["email"] = email
            return render_template("index.html", welcome_user=session.get("email"))
        else:
            session.pop("email", None)
            return render_template("sign_in/bad_credentials.html", welcome_user=session.get("email"))


@sign_up_sign_in_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "GET":
        return render_template("sign_up/registration.html", welcome_user=session.get("email"))

    else:
        email = request.form.get("email")
        password = request.form.get("p1")

        if UserModel.find_by_email(email):
            return render_template("sign_up/already_exists.html", welcome_user=session.get("email"))

        new_user = UserModel(email, UserModel.generate_hash(password))
        new_user.save_to_db()
        session["email"] = email
        return render_template("sign_up/successful.html", welcome_user=session.get("email"))


@sign_up_sign_in_bp.route('/sign_out')
def sign_out():
    session.pop("email", None)
    return render_template("index.html")
