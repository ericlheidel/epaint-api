#!/bin/bash

rm db.sqlite3
rm -rf ./epaintapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations epaintapi
python3 manage.py migrate epaintapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata userinfos
python3 manage.py loaddata painttypes
python3 manage.py loaddata paints_black
python3 manage.py loaddata paints_gold
python3 manage.py loaddata paints_white
python3 manage.py loaddata paints_special
python3 manage.py loaddata sizes
python3 manage.py loaddata payments
python3 manage.py loaddata orders_user1
python3 manage.py loaddata orders_user2
# python3 manage.py loaddata orderpaints_user1
python3 manage.py loaddata orderpaints_user2
python3 manage.py loaddata userimages