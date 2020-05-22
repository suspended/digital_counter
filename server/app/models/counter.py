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
        result = db.session.query(func.max(cls.time)).first()
        if result is None:
            return None
        else:
            return result
        