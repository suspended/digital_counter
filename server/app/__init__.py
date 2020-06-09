from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_caching import CachingQuery
from flask_caching import Cache
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from flask_cors import CORS

from app.config import Config

db = SQLAlchemy(query_class=CachingQuery)
migrate = Migrate()
jwt = JWTManager()
scheduler = APScheduler()
cache = Cache()

@scheduler.task('cron', id='clear_old_records', hour=0)
def clear_count_job():
    with scheduler.app.app_context():
        from app.models.counter import Counter
        Counter.clear_expired_count()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    cache.init_app(app)
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
