from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main_route import main_blueprint
    from app.routes.user_route import user_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)

    return app
