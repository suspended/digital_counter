#! /bin/bash

export FLASK_APP=run.py
export FLASK_ENV=development
export DATABASE_URI='postgres://admin:admin@localhost:5432/dc_db'

flask db upgrade
flask run