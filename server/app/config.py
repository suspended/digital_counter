import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-very-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'my-very-secret-key'

    SCHEDULER_API_ENABLED = True

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 600
