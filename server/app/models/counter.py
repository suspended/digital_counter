from sqlalchemy.sql import func

from datetime import datetime

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

    def get_latest_count(self):
        if not self.counters:
            Counter.create_count(self.id, 0)

        latest_count = self.counters[0]
        max_time = self.counters[0].time
        for counter in self.counters:
            if counter.time > max_time:
                latest_count = counter
        return counter

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
