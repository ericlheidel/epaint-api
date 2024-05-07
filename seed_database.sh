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
python3 manage.py loaddata orders
# python3 manage.py loaddata orders_user1
# python3 manage.py loaddata orders_user2
# python3 manage.py loaddata userimages


# Below is an example of the opposite of the above
# The below example will dump data from the .sqlite3 file and create a fixture of the JSON data
# The below example takes the model "orderpaint" from app "epaintapi" and writes the JSON into a fixture # # # file called "test.json"

# here is the command line:
# python manage.py dumpdata epaintapi.orderpaint --indent 2 > epaintapi/fixtures/test.json