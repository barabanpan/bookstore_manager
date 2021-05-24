from flask.blueprints import Blueprint
from flask import render_template, request, session
import base64

from app.models.manager_model import ManagerModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/sign_in', methods=['GET'])
def sign_in():
    basic_auth = request.headers.get("Authorization")
    if not basic_auth:
        return "Unauthorized", 401
    token = (basic_auth + " ").split()[1]
    decoded = base64.b64decode(token).decode('utf-8')
    try:
        [email, password] = decoded.split(":")
    except Exception:
        return "Unauthorized", 401

    manager = ManagerModel.find_by_email(email)
    if not manager:
        return "Unauthorized", 401
    right_pass = ManagerModel.verify_hash(password, manager.hash_password)
    if right_pass:
        session["email"] = email
        return "ok", 200  # повернути 2 токени
    else:
        session.pop("email", None)
        return "Unauthorized", 401


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    if not request.json:
        return "No json data provided.", 400
    email = request.json.get("email")
    name = request.json.get("name")
    password = request.json.get("password")

    if ManagerModel.find_by_email(email):
        return "An account with the given email already exists.", 400 

    if not (email and name and password):
        return "'email', 'name' and 'password' are required.", 400
    new_manager = ManagerModel(email, name, ManagerModel.generate_hash(password))
    new_manager.save_to_db()
    session["email"] = email
    return "New manager signed up.", 200


@auth_bp.route('/refresh')
def refresh_access_token():
    # ???
    session.pop("email", None)
    # take email from token, get token, expire them
    return render_template("index.html")


@auth_bp.route('/expire_access')
def sign_out_access():
    session.pop("email", None)
    # take email from token, get token, expire them
    return render_template("index.html")


@auth_bp.route('/expire_refresh')
def sign_out_refresh():
    session.pop("email", None)
    # take email from token, get token, expire them
    return render_template("index.html")
