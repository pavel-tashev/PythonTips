from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required


appExample = Blueprint("appExample", __name__)

@appExample.route('/')
def home() -> tuple:
    return jsonify([]), 200

@appExample.route('/profile')
@login_required
def profile() -> tuple:
    return jsonify(
        {
            'username': current_user.username,
            'email': current_user.email
        }
    ), 200