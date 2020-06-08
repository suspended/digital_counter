#! /bin/bash

export FLASK_APP=run.py
export FLASK_ENV=development
export DATABASE_URI=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

flask db upgrade
gunicorn --bind 0.0.0.0:5000 --workers=3 run:app