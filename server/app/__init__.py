from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    db = SQLAlchemy()
    db.init_app(app)

    from app.routes.main_route import main_blueprint
    from app.routes.user_route import user_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)

    return app
