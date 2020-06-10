from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from flask_cors import CORS

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
scheduler = APScheduler()

@scheduler.task('cron', id='clear_old_records', hour=0)
def clear_count_job():
    with scheduler.app.app_context():
        from app.models.counter import Counter
        Counter.clear_expired_count()

@scheduler.task('interval', id='calculate_stats', minutes=10)
def calculate_stats_job():
    print("running calculate stats")
    with scheduler.app.app_context():
        from app.models.counter import Location, CounterStat

        locations = Location.get_all_location()

        for location in locations:
            CounterStat.the_cron_job_function(location.id)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    scheduler.init_app(app)
    CORS(app)

    scheduler.start()

    from app.routes.main_route import main_blueprint
    from app.routes.user_route import user_blueprint
    from app.routes.counter_route import counter_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(counter_blueprint)

    return app
