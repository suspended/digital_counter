import os

from sqlalchemy.sql import func
from datetime import datetime, timedelta

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

