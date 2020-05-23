from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, create_access_token
from datetime import datetime, timedelta

from app.models.counter import Counter, Threshold

counter_blueprint = Blueprint('counter_blueprint', __name__)

@counter_blueprint.route('/get_counter', methods=['GET'])
def get_counter():
    counter = Counter.get_latest_count()
    return jsonify({
        "count": counter.count,
        "last_updated": counter.time
    }), 200

@counter_blueprint.route('/update_counter', methods=['POST'])
def update_counter():
    count = request.values['count']
    counter = Counter.create_count(count)
    return jsonify({
        "count": counter.count,
        "last_updated": counter.time
    }), 200

@counter_blueprint.route('/get_threshold', methods=['GET'])
def get_threshold():
    return 200

@counter_blueprint.route('/update_threshold', methods=['POST'])
def update_threshold():
    return 200
