from flask_login import (
    login_user,
    logout_user,
    current_user,
    LoginManager,
    login_required
)
from flask_session import Session
from flask import Blueprint, request, jsonify

from .validators import register_validator, login_validator

# SQLAlchemy
from .models.sqlaModels import User
# END SQLAlchemy

# MongoDb
# from .models.mongodbModels import User
# END MongoDb


session = Session()
appAuth = Blueprint("appAuth", __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id: int):
    if user_id is not None:
        return User.get_by_id(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized() -> tuple:
    return jsonify({'message': 'Access denied!'}), 401



@appAuth.route('/v1/auth/register', methods=['POST'])
def register() -> tuple:
    data = request.get_json(silent = True)
    try:
        register_validator(data)
    except Exception as e:
        return jsonify({'message': e.args[0]['message']}), e.args[0]['code']

    email = data['email']
    password = data['password']
    username = email

    try:
        User.register(email, username, password)
        return jsonify([]), 201
    except Exception as e:
        return jsonify({'message': 'Email address already occipied!'}), 409

@appAuth.route('/v1/auth/login', methods=['POST'])
def login() -> tuple:
    data = request.get_json(silent = True)
    try:
        login_validator(data)
    except Exception as e:
        return jsonify({'message': e.args[0]['message']}), e.args[0]['code']

    email_or_username = data['email_or_username']
    password = data['password']

    try:
        user = User.get_verified(email_or_username, password)
        login_user(user)
        return jsonify([]), 200
    except Exception as e:
        return jsonify({'message': 'Invalid credentials!'}), 404

@appAuth.route('/v1/auth/logout', methods=['POST'])
@login_required
def logout() -> tuple:
    logout_user()
    return jsonify([]), 200