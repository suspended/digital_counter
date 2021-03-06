import os
import sys
import math
import pytz

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.sql import func
from datetime import date, time, datetime, timedelta

from app import db


class Location(db.Model):
    __tablename__ = "Location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    ok_limit = db.Column(db.Integer, nullable=False)
    warning_limit = db.Column(db.Integer, nullable=False)
    last_notified = db.Column(db.DateTime, nullable=True)
    notify_email_addresses = db.Column(db.Text, default="", server_default="", nullable=False)
    notify_interval = db.Column(db.Integer, default=3, server_default="3", nullable=False)
    notify_ok_trigger = db.Column(db.Boolean, server_default="false", nullable=False)
    notify_warning_trigger = db.Column(db.Boolean, server_default="false", nullable=False)

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
    
    @staticmethod
    def update_notification_settings(location_id, email_addresses, interval):
        location = Location.query.filter_by(id=location_id).first()
        if location is None:
            return None
        else:
            location.notify_email_addresses = email_addresses
            location.notify_interval = interval
            db.session.commit()
        return location 

    def notify_email(self, count):
        message_content = ""

        current_time = datetime.utcnow()
        if count > self.warning_limit:
            if self.notify_warning_trigger is False:
                self.notify_ok_trigger = True
                self.notify_warning_trigger = True
                self.last_notified = current_time
                db.session.commit() # commit early to prevent other workers from sending email as well
                message_content = "The crowd  in " + self.name + " has now reached more than " + str(self.warning_limit) + " pax"
            else:
                return
        elif count > self.ok_limit:
            if self.notify_ok_trigger is False:
                self.notify_ok_trigger = True
                self.last_notified = current_time
                db.session.commit() # commit early to prevent other workers from sending email as well
                message_content = "The crowd  in " + self.name + " has now reached more than " + str(self.ok_limit) + " pax"
            else:
                return
        else:
            if self.last_notified is None or self.last_notified == "" or(current_time - self.last_notified > timedelta(minutes=self.notify_interval)):
                self.notify_ok_trigger = False
                self.notify_warning_trigger = False
                db.session.commit() # commit early to prevent other workers from sending email as well
            return

        try:
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            #The mail addresses and password
            sender_address = os.environ.get('EMAIL_USER', '')
            sender_pass = os.environ.get('EMAIL_PASSWORD', '')
            session.login(sender_address, sender_pass) #login with mail_id and password

            for email in (self.notify_email_addresses).split(','):
                #Setup the MIME
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = email
                message['Subject'] = 'Crowd Status'   #The subject line
                #The body and the attachments for the mail
                message.attach(MIMEText(message_content, 'plain'))
                text = message.as_string()
                session.sendmail(sender_address, email, text)
            session.quit()
        except Exception as e:
            print(e)
            print("Fail to send email. Make sure the following are done if you want this feature")
            print("1) Set environment variables EMAIL_USER and EMAIL_PASSWORD")
            print("\t For deployment, this can be set on the docker-compose.env file")
            print("2) Make sure your email server(eg. gmail) settings are configured for it")
        
            

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

            counter.location.notify_email(counter.count)
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
            target_date = datetime.utcnow() - timedelta(days=6-i)
            target_date = target_date.replace(tzinfo=pytz.utc)
            sgt = pytz.timezone("Asia/Singapore")
            for target_hour in range(24):
                target_datetime = datetime.combine(target_date.date(), time(hour=target_hour))
                target_datetime = target_datetime.replace(tzinfo=pytz.utc)
                sgt_datetime = target_datetime.astimezone(sgt)

                query = db.session.query(cls).filter(
                    cls.location_id==location_id,
                    cls.date==sgt_datetime.date(),
                    cls.hour==sgt_datetime.hour
                )
                record = query.first()
                if record is None:
                    records = Counter.get_statistics(
                        location_id,
                        target_datetime,
                        target_datetime+ timedelta(hours=1)
                    )
                    counterStat = CounterStat(
                        location_id,
                        sgt_datetime.date(),
                        sgt_datetime.hour,
                        calculate_max(records),
                        calculate_min(records),
                        calculate_avg(records)
                    )
                    db.session.add(counterStat)
                    db.session.commit()

    @classmethod
    def update_daily_stats(cls, location_id):
        # check previous days records
        cls.check_previous_days_exists(location_id)
        
        # get datetiume for the the current and past record
        current = datetime.now()
        current = current.replace(tzinfo=pytz.utc)
        current = current.replace(minute=0)
        current = current.replace(second=0)
        current = current.replace(microsecond=0)
        past_1 = current
        past_1 = past_1 - timedelta(hours=1)
        local = pytz.timezone("Asia/Singapore")

        # get 2 latest counter records
        past_1_records = Counter.get_statistics(
            location_id, 
            past_1, 
            past_1 + timedelta(hours=1)
        )
        current_records = Counter.get_statistics(
            location_id, 
            current, 
            current + timedelta(hours=1)
        )

        sgt = pytz.timezone("Asia/Singapore")
        sgt_current = current.astimezone(sgt)
        sgt_past_1 = past_1.astimezone(sgt)

        # update 2 latest record (incase miss any)
        past_1_counterstat = cls.query.filter(
            cls.location_id == location_id,
            cls.date == sgt_past_1.date(),
            cls.hour == sgt_past_1.hour
        ).first()
        past_1_counterstat.max_count = calculate_max(past_1_records)
        past_1_counterstat.min_count = calculate_min(past_1_records)
        past_1_counterstat.avg_count = calculate_avg(past_1_records)

        current_counterstat = cls.query.filter(
            cls.location_id == location_id,
            cls.date == sgt_current.date(),
            cls.hour == sgt_current.hour
        ).first()
        current_counterstat.max_count = calculate_max(current_records)
        current_counterstat.min_count = calculate_min(current_records)
        current_counterstat.avg_count = calculate_avg(current_records)

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
