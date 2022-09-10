from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user

# SQLAlchemy
from auth.models.sqlaModels import User
# END SQLAlchemy

# MongoDb
# from auth.models.mongodbModels import User
# END MongoDb


appExample = Blueprint("appExample", __name__)

@appExample.route('/')
def home() -> tuple:
    return jsonify([]), 200

@appExample.route('/profile')
@jwt_required()
def profile() -> tuple:
    sessions = User.get_sessions(current_user.id)
    return jsonify(
        {
            'username': current_user.username,
            'email': current_user.email,
            'sessions': [
                {
                    'access_token': session.jti_access,
                    'created_at': session.created_at
                }
                for session in sessions
            ]
        }
    ), 200