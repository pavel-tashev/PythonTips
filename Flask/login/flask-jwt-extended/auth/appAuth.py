from flask_jwt_extended import (
    get_jwt,
    JWTManager,
    decode_token,
    jwt_required,
    current_user,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)

from flask import Blueprint, request, jsonify

from .validators import (
    login_validator,
    register_validator,
    revoke_tokens_validator
)

# SQLAlchemy
from .models.sqlaModels import User, Session
# END SQLAlchemy

# MongoDb
# from .models.mongodbModels import User, Session
# END MongoDb


jwt = JWTManager()
appAuth = Blueprint("appAuth", __name__)

@jwt.user_identity_loader
def user_identity_lookup(sub):
    id = sub['id'] if type(sub) is dict else sub
    return id

@jwt.user_lookup_loader
def user_lookup_callback(jwt_header: dict, jwt_data: dict) -> User:
    sub = jwt_data["sub"]
    id = sub['id'] if type(sub) is dict else sub
    return User.get_by_id(id)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header: dict, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]

    if jwt_payload['type'] == 'access':
        return Session.get_by_jti_access(jti) is None

    if jwt_payload['type'] == 'refresh':
        return Session.get_by_jti_refresh(jti) is None

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header: dict, jwt_payload: dict) -> tuple:
    return jsonify({'msg': 'Access denied!'}), 401



@appAuth.route('/v1/auth/register', methods=['POST'])
def register() -> tuple:
    data = request.get_json(silent = True)
    try:
        register_validator(data)
    except Exception as e:
        return jsonify({'msg': e.args[0]['msg']}), e.args[0]['code']

    email = data['email']
    password = data['password']
    username = email

    try:
        user = User.register(email, username, password)
        identity = __get_user_identity(user)

        access_token = create_access_token(identity = identity)
        refresh_token = create_refresh_token(identity = identity)

        jti_access = decode_token(access_token)['jti']
        jti_refresh = decode_token(refresh_token)['jti']
        Session.add(user.id, jti_access, jti_refresh)

        return jsonify(
            {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        ), 201
    except Exception as e:
        return jsonify({'msg': 'Email address already occipied!'}), 409

@appAuth.route('/v1/auth/login', methods=['POST'])
def login() -> tuple:
    data = request.get_json(silent = True)
    try:
        login_validator(data)
    except Exception as e:
        return jsonify({'msg': e.args[0]['msg']}), e.args[0]['code']

    email_or_username = data['email_or_username']
    password = data['password']

    try:
        user = User.get_verified(email_or_username, password)
        identity = __get_user_identity(user)

        access_token = create_access_token(identity = identity)
        refresh_token = create_refresh_token(identity = identity)

        jti_access = decode_token(access_token)['jti']
        jti_refresh = decode_token(refresh_token)['jti']
        Session.add(user.id, jti_access, jti_refresh)

        return jsonify(
            {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        ), 200
    except Exception as e:
        return jsonify({'msg': 'Invalid credentials!'}), 404

@appAuth.route("/v1/auth/refresh", methods = ["POST"])
@jwt_required(refresh = True)
def refresh() -> tuple:
    jti_refresh_old = get_jwt()["jti"]

    identity = get_jwt_identity()
    access_token = create_access_token(identity = identity)
    refresh_token = create_refresh_token(identity = identity)

    jti_access = decode_token(access_token)['jti']
    jti_refresh = decode_token(refresh_token)['jti']
    Session.refresh(jti_refresh_old, jti_access, jti_refresh)

    return jsonify(
        {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    ), 201

@appAuth.route('/v1/auth/logout', methods = ['POST'])
@jwt_required()
def logout() -> tuple:
    jti_access = get_jwt()["jti"]
    Session.delete(jti_access)
    return jsonify([]), 200

@appAuth.route('/v1/auth/revoke-tokens', methods = ['DELETE'])
@jwt_required()
def revoke_tokens() -> tuple:
    data = request.get_json(silent = True)
    try:
        revoke_tokens_validator(data)
    except Exception as e:
        return jsonify({'msg': e.args[0]['msg']}), e.args[0]['code']

    for jti_access in data['tokens']:
        Session.delete(current_user.id, jti_access)

    return jsonify([]), 200

def __get_user_identity(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }