from flask import Blueprint

from app.models.user import User

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/login')
def index():
    return "login"
