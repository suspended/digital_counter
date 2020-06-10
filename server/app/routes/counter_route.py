from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta, date

import sys
import math
import pytz

from app.models.counter import Counter, Location, CounterStat

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

@counter_blueprint.route('/location/statistics', methods=['POST'])
def get_location_stats():
    location_id = request.values['location_id']
    # start_time = datetime.strptime(request.values['start_time'], '%a, %d %b %Y %H:%M:%S %Z')
    # end_time = datetime.strptime(request.values['end_time'], '%a, %d %b %Y %H:%M:%S %Z')
    start_time = datetime.strptime(request.values['start_time'], '%Y-%m-%dT%H:%M')
    end_time = datetime.strptime(request.values['end_time'], '%Y-%m-%dT%H:%M')

    local = pytz.timezone("Asia/Singapore")
    local_start_time = local.localize(start_time, is_dst=None)
    local_end_time = local.localize(end_time, is_dst=None)
    utc_start_time = local_start_time.astimezone(pytz.utc)
    utc_end_time = local_end_time.astimezone(pytz.utc)

    stats = Counter.get_statistics(location_id, utc_start_time, utc_end_time)

    data = []

    for stat in stats:
        data.append({
            'count': stat.count,
            'time' : stat.time
        })

    return jsonify({
        'stats': data
    }), 200

@counter_blueprint.route('/location/daily_statistics', methods=['POST'])
def get_daily_stats():
    location_id = request.values['location_id']
    target_date = date.fromisoformat(request.values['target_date'])

    records = CounterStat.get_day_stats(1, target_date)
    data = []

    for record in records:
        data.append({
            "location_id": record.location_id,
            "max": record.max_count,
            "min": record.min_count,
            "avg": record.avg_count,
            "hour": record.hour,
            "date": record.date.isoformat()
        })

    data = sorted(data, key=lambda i: i['hour'])

    return jsonify(data), 200

@counter_blueprint.route('/run_cron', methods=['GET'])
def activate_cron_job():

    locations = Location.get_all_location()

    start = datetime.now()
    for location in locations:
        CounterStat.the_cron_job_function(location.id)
    end = datetime.now()

    today = date.today()
    todayStats = CounterStat.get_day_stats(1, today)

    data = []

    for record in todayStats:
        data.append({
            "location_id": record.location_id,
            "max": record.max_count,
            "min": record.min_count,
            "avg": record.avg_count,
            "hour": record.hour,
            "date": record.date.isoformat()
        })

    return jsonify({
        "time_taken": (str(start) + " --- " + str(end)),
        "data": data
    }), 200

@counter_blueprint.route('/run_cron_update', methods=['GET'])
def activate_cron_update():

    locations = Location.get_all_location()

    start = datetime.now()
    for location in locations:
        CounterStat.cron_job_update(location.id)
    end = datetime.now()

    today = date.today()
    todayStats = CounterStat.get_day_stats(1, today)

    data = []

    for record in todayStats:
        data.append({
            "location_id": record.location_id,
            "max": record.max_count,
            "min": record.min_count,
            "avg": record.avg_count,
            "hour": record.hour,
            "date": record.date.isoformat()
        })

    return jsonify({
        "time_taken": (str(start) + " --- " + str(end)),
        "data": data
    }), 200

def calculate_max(records):
    max_count = 0
    for record in records:
        if record.count > max_count:
            max_count = record.count

    return max_count

def calculate_min(records):
    min_count = sys.maxsize
    for record in records:
        if record.count < min_count:
            min_count = record.count
    
    if min_count == sys.maxsize:
        min_count = 0
    
    return min_count

def calculate_avg(records):
    total = 0

    if len(records) == 0:
        return 0;

    for record in records:
        total = total + record.count
    
    
    return math.ceil(total/len(records))
