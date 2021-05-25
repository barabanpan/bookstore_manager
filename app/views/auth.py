from flask.blueprints import Blueprint
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt)
import base64

from app.models.manager_model import ManagerModel
from app.models.revoked_token_model import RevokedTokenModel

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
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return {
            "message": "Logged in as {}".format(email),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }, 200
    else:
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

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    return {
        "message": "Logged in as {}".format(email),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }, 200


@auth_bp.route('/refresh')
@jwt_required(refresh=True)
def refresh_access_token():
    email = get_jwt_identity()
    access_token = create_access_token(identity=email)
    return {
        'access_token': access_token,
        "token_type": "Bearer"
    }, 200


@auth_bp.route('/sign_out_access')
@jwt_required()
def sign_out_access():
    jti = get_jwt()['jti']
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {'message': 'Access token has been revoked'}
    except Exception:
        return {"message": "Something went wrong while revoking token"}, 500


@auth_bp.route('/sign_out_refresh')
@jwt_required(refresh=True)
def sign_out_refresh():
    jti = get_jwt()['jti']  # id of a jwt accessing this post method
    try:
        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()
        return {"message": "Refresh token has been revoked"}, 200
    except Exception:
        return {"message": "Something went wrong while revoking token"}, 500
