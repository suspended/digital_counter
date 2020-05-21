import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-very-secret-key'
    SQL_ALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///mydb.sqlite'
