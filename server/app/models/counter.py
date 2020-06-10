import os
import sys
import math
import pytz

from sqlalchemy.sql import func
from datetime import date, time, datetime, timedelta

from app import db


class Location(db.Model):
    __tablename__ = "Location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False);
    ok_limit = db.Column(db.Integer, nullable=False)
    warning_limit = db.Column(db.Integer, nullable=False)

    counters = db.relationship("Counter", back_populates="location")

    def __init__(self, name, ok_limit, warning_limit):
        self.name = name
        self.ok_limit = ok_limit
        self.warning_limit = warning_limit

    @staticmethod
    def create_location(name):
        location = Location(name=name, ok_limit=50, warning_limit=80)
        try:
            db.session.add(location)
            db.session.commit()
        except:
            return None
        return location

    @staticmethod
    def get_location(id):
        location = Location.query.filter_by(id=id).first()
        return location

    @staticmethod
    def get_all_location():
        result = Location.query.all()
        return result

    @staticmethod
    def update_threshold(id, ok_limit, warning_limit):
        location = Location.query.filter_by(id=id).first()
        if location is None:
            return None
        else:
            location.ok_limit = ok_limit
            location.warning_limit = warning_limit
            db.session.commit()
        return location
    

class Counter(db.Model):
    __tablename__ = "Counter"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'), nullable=False)

    location = db.relationship("Location", back_populates="counters")

    def __init__(self, id, count):
        self.location_id = id
        self.count = count
        self.time = datetime.utcnow()

    @staticmethod
    def create_count(id, count):
        counter = Counter(id=id, count=count)
        try:
            db.session.add(counter)
            db.session.commit()
        except:
            return None
        return counter 

    @classmethod
    def get_location_latest_count(cls):
        subquery = db.session.query(cls.location_id.label('target_location'), func.max(cls.time).label('max_time')).group_by(cls.location_id).subquery()    
        query = db.session.query(cls.location_id, cls.count, cls.time).filter(
            cls.location_id==subquery.c.target_location,
            cls.time==subquery.c.max_time
        )
        result = query.all()
        return result 

    @classmethod
    def get_statistics(cls, location_id, start_time, end_time):
        results = db.session.query(cls).filter(
            cls.location_id==location_id,
            cls.time >= start_time,
            cls.time <= end_time
        ).all()
        return results

    @classmethod
    def clear_expired_count(cls, expiry_days=7):
        limit = datetime.now() - timedelta(days=expiry_days)
        cls.query.filter(cls.time < limit).delete()
        db.session.commit()

class CounterStat(db.Model):
    __tablename__ = "CounterStat"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    max_count = db.Column(db.Integer, nullable=False)
    min_count = db.Column(db.Integer, nullable=False)
    avg_count = db.Column(db.Integer, nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('Location.id'), nullable=False)

    def __init__(self, location_id, date, hour, max_count=0, min_count=0, avg_count=0):
        self.location_id = location_id
        self.date = date
        self.hour = hour
        self.max_count = max_count
        self.min_count = min_count
        self.avg_count = avg_count

    @classmethod
    def get_day_stats(cls, location_id, target_date):
        records = cls.query.filter(cls.location_id==location_id,cls.date==target_date).all()
        return records

    @classmethod
    def check_previous_days_exists(cls, location_id):
        # creates if not exist
        for i in range(7):
            local = pytz.timezone("Asia/Singapore")
            target_date = date.today() - timedelta(days=7-1-i)
            for target_hour in range(24):
                query = db.session.query(cls).filter(
                    cls.location_id==location_id,
                    cls.date==target_date,
                    cls.hour==target_hour
                )
                record = query.first()
                if record is None:
                    records = Counter.get_statistics(
                        location_id,
                        (local.localize(datetime.combine(target_date, time(hour=target_hour)), is_dst=None)).astimezone(pytz.utc),
                        (local.localize(datetime.combine(target_date, time(hour=target_hour))+ timedelta(hours=1), is_dst=None)).astimezone(pytz.utc)
                    )
                    counterStat = CounterStat(
                        location_id,
                        target_date,
                        target_hour,
                        calculate_max(records),
                        calculate_min(records),
                        calculate_avg(records)
                    )
                    db.session.add(counterStat)
                    db.session.commit()

    @classmethod
    def the_cron_job_function(cls, location_id):
        # check previous days records
        cls.check_previous_days_exists(location_id)
        
        # get datetiume for the the current and past record
        current = datetime.now()
        current = current.replace(minute=0)
        current = current.replace(second=0)
        current = current.replace(microsecond=0)
        past_1 = current
        past_1 = past_1 - timedelta(hours=1)
        local = pytz.timezone("Asia/Singapore")

        # get 2 latest counter records
        past_1_records = Counter.get_statistics(
            location_id, 
            local.localize(past_1, is_dst=None).astimezone(pytz.utc), 
            local.localize(past_1 + timedelta(hours=1), is_dst=None).astimezone(pytz.utc)
        )
        current_records = Counter.get_statistics(
            location_id, 
            local.localize(current,is_dst=None).astimezone(pytz.utc), 
            local.localize(current + timedelta(hours=1), is_dst=None).astimezone(pytz.utc)
        )

        # update 2 latest record (incase miss any)
        past_1_counterstat = cls.query.filter(
            cls.location_id == location_id,
            cls.date == past_1.date(),
            cls.hour == past_1.hour
        ).first()
        past_1_counterstat.max_count = calculate_max(past_1_records)
        past_1_counterstat.min_count = calculate_min(past_1_records)
        past_1_counterstat.avg_count = calculate_avg(past_1_records)

        current_counterstat = cls.query.filter(
            cls.location_id == location_id,
            cls.date == current.date(),
            cls.hour == current.hour
        ).first()
        current_counterstat.max_count = calculate_max(current_records)
        current_counterstat.min_count = calculate_min(current_records)
        current_counterstat.avg_count = calculate_avg(current_records)

        db.session.commit()

    @classmethod
    def cron_job_update(cls, location_id):
        # get datetiume for the the current and past record
        current = datetime.now()
        current = current.replace(minute=0)
        current = current.replace(second=0)
        current = current.replace(microsecond=0)
        past_1 = current
        past_1 = past_1 - timedelta(hours=1)
        local = pytz.timezone("Asia/Singapore")

        print("Current no zone: " + str(current), flush=True)
        print("past1 no zone: " + str(past_1), flush=True)

        # get 2 latest counter records
        past_1_records = Counter.get_statistics(
            location_id, 
            local.localize(past_1, is_dst=None).astimezone(pytz.utc), 
            local.localize(past_1 + timedelta(hours=1), is_dst=None).astimezone(pytz.utc)
        )
        current_records = Counter.get_statistics(
            location_id, 
            local.localize(current,is_dst=None).astimezone(pytz.utc), 
            local.localize(current + timedelta(hours=1), is_dst=None).astimezone(pytz.utc)
        )

        print("Current post zone: " + str(current), flush=True)
        print("past1 post zone: " + str(past_1), flush=True)
        print("Size past record", flush=True)
        print(len(past_1_records), flush=True)
        print("Size current record", flush=True)
        print(len(current_records), flush=True)

        # update 2 latest record (incase miss any)
        past_1_counterstat = cls.query.filter(
            cls.location_id == location_id,
            cls.date == past_1.date(),
            cls.hour == past_1.hour
        ).first()
        print("past 1 obj", flush=True)
        print(past_1_counterstat.avg_count, flush=True)
        past_1_counterstat.max_count = calculate_max(past_1_records)
        past_1_counterstat.min_count = calculate_min(past_1_records)
        past_1_counterstat.avg_count = calculate_avg(past_1_records)
        print(past_1_counterstat.avg_count, flush=True)

        current_counterstat = cls.query.filter(
            cls.location_id == location_id,
            cls.date == current.date(),
            cls.hour == current.hour
        ).first()
        print("current obj", flush=True)
        print(current_counterstat.avg_count, flush=True)
        current_counterstat.max_count = calculate_max(current_records)
        current_counterstat.min_count = calculate_min(current_records)
        current_counterstat.avg_count = calculate_avg(current_records)
        print(current_counterstat.avg_count, flush=True)

        db.session.commit()

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

    if len(records) == 0 or records is None:
        return 0;

    for record in records:
        total = total + record.count
    
    
    return math.ceil(total/len(records))
