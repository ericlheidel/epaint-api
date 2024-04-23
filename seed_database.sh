#!/bin/bash

rm db.sqlite3
rm -rf ./epaintapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations epaintapi
python3 manage.py migrate epaintapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata painttypes
python3 manage.py loaddata paints

