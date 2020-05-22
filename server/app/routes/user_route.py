from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token

from app.models.user import User

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/login', methods=['POST'])
def index():
    username = request.values['username']
    password = request.values['password']

    if not username:
        return 'No Username', 404
    if not password:
        return 'No Password', 404
    
    user = User.login_user(username=username, password=password)
    if user is None:
        return 'Login Failed', 400

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@user_blueprint.route('/register', methods=['POST'])
def register():
    username = request.values['username']
    password = request.values['password']

    if not username:
        return 'No Username', 404
    if not password:
        return 'No Password', 404
    
    user = User.create_user(username=username, password=password)
    if user is None:
        return 'Registration Failed', 400

    return 'Registration Successful', 200