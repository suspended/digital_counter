#! /bin/bash

export FLASK_APP=run.py
export FLASK_ENV=development
export DATABASE_URI='postgres://admin:admin@localhost:5432/dc_db'

flask db migrate
flask db upgrade
gunicorn --bind 0.0.0.0:5000 run:app