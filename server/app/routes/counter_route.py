from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

from app.models.counter import Counter, Location

counter_blueprint = Blueprint('counter_blueprint', __name__)

@counter_blueprint.route('/location/get_latest_count', methods=['GET'])
def get_counter():
    counters = Counter.get_location_latest_count()
    data = []

    for counter in counters:
        location = Location.get_location(counter.location_id)
        data.append({
            "id": location.id,
            "name": location.name,
            "ok_limit": location.ok_limit,
            "warning_limit": location.warning_limit,
            "count": counter.count,
            "last_updated": counter.time
        })
    data.sort(key=lambda x: x["id"])
    return jsonify(data), 200

@counter_blueprint.route('/location/update_counter', methods=['POST'])
@jwt_required
def update_counter():
    id = request.values['id']
    count = request.values['count']
    if int(count) < 0:
        count = 0
    counter = Counter.create_count(id, count)
    
    return jsonify({
        "count": counter.count,
        "last_updated": counter.time
    }), 200

@counter_blueprint.route('/location', methods=['PUT'])
@jwt_required
def create_location():
    name = request.values['name']

    location = Location.create_location(name=name)

    return jsonify({
        "id": location.id,
        "name": location.name,
        "ok_limit": location.ok_limit,
        "warning_limit": location.warning_limit
    }), 200

@counter_blueprint.route('/location', methods=['GET'])
def get_locations():
    locations = Location.get_all_location()

    data = []

    for location in locations:
        data.append({
            "id": location.id,
            "name": location.name,
            "ok_limit": location.ok_limit,
            "warning_limit": location.warning_limit
        })

    return jsonify(data),  200

@counter_blueprint.route('/location/update_threshold', methods=['POST'])
@jwt_required
def update_location_threshold():
    id = request.values['id']
    ok_limit = request.values['ok_limit']
    warning_limit = request.values['warning_limit']

    location = Location.update_threshold(id, ok_limit, warning_limit)

    return jsonify({
        "ok_limit": location.ok_limit,
        "warning_limit": location.warning_limit
    }),  200
