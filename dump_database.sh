# python3 manage.py dumpdata auth_user --indent 2 > epaintapi/fixtures/users_test.json
# python3 manage.py dumpdata authtoken_token --indent 2 > epaintapi/fixtures/tokens_test.json
python3 manage.py dumpdata epaintapi.userinfo --indent 2 > epaintapi/fixtures/userinfos_test.json
python3 manage.py dumpdata epaintapi.painttype --indent 2 > epaintapi/fixtures/painttypes_test.json
python3 manage.py dumpdata epaintapi.paint --indent 2 > epaintapi/fixtures/paints_test.json
python3 manage.py dumpdata epaintapi.size --indent 2 > epaintapi/fixtures/sizes_test.json
python3 manage.py dumpdata epaintapi.payment --indent 2 > epaintapi/fixtures/payments_test.json
python3 manage.py dumpdata epaintapi.order --indent 2 > epaintapi/fixtures/orders_test.json
python3 manage.py dumpdata epaintapi.orderpaint --indent 2 > epaintapi/fixtures/orderpaints_test.json
# python3 manage.py dumpdata epaintapi.userimages --indent 2 > epaintapi/fixtures/userimages_test.json



# python manage.py dumpdata epaintapi.orderpaint --indent 2 > epaintapi/fixtures/test.json