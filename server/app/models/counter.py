from sqlalchemy.sql import func

from datetime import datetime

from app import db

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self, count):
        self.count = count
        self.time = datetime.now()

    @staticmethod
    def create_count(count):
        counter = Counter(count)
        try:
            db.session.add(counter)
            db.session.commit()
        except:
            return None
        return counter

    @classmethod
    def get_latest_count(cls):
        result = db.session.query(cls).filter(cls.time==func.max(cls.time).select()).first()
        if result is None:
            result = Counter.create_count(0)
            return result
        else:
            return result
            

class Threshold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ok_limit = db.Column(db.Integer, nullable=False)
    warning_limit = db.Column(db.Integer, nullable=False)

    def __init__(self, ok_limit, warning_limit):
        self.ok_limit = ok_limit
        self.warning_limit = warning_limit

    @staticmethod
    def get_threshold():
        result = Threshold.query.first()
        if result is None:
            result = Threshold(50, 80)
            db.session.add(result)
            db.session.commit()
        return result

    @staticmethod
    def update_threshold(ok_limit, warning_limit):
        result = Threshold.query.first()
        if result is None:
            result = Threshold(ok_limit, warning_limit)
            db.session.add(result)
            db.session.commit()
        else:
            result.ok_limit = ok_limit
            result.warning_limit = warning_limit
            db.session.commit()
        return result
