# USERS
# python3 manage.py dumpdata auth_user --indent 2 > epaintapi/fixtures/users_test.json

# TOKENS
# python3 manage.py dumpdata authtoken_token --indent 2 > epaintapi/fixtures/tokens_test.json

# USERINFO
# python3 manage.py dumpdata epaintapi.userinfo --indent 2 > epaintapi/fixtures/userinfos_test.json

# PAINTTYPE
# python3 manage.py dumpdata epaintapi.painttype --indent 2 > epaintapi/fixtures/painttypes_test.json

# PAINT
# python3 manage.py dumpdata epaintapi.paint --indent 2 > epaintapi/fixtures/paints_test.json

# SIZE
# python3 manage.py dumpdata epaintapi.size --indent 2 > epaintapi/fixtures/sizes_test.json

# PAYMENT
# python3 manage.py dumpdata epaintapi.payment --indent 2 > epaintapi/fixtures/payments_test.json

# ORDER
python3 manage.py dumpdata epaintapi.order --indent 2 > epaintapi/fixtures/orders_test.json

# ORDERPAINT
# python3 manage.py dumpdata epaintapi.orderpaint --indent 2 > epaintapi/fixtures/orderpaints_test.json

# USERIMAGES
# python3 manage.py dumpdata epaintapi.userimages --indent 2 > epaintapi/fixtures/userimages_test.json




# EXAMPLE
# python manage.py dumpdata epaintapi.orderpaint --indent 2 > epaintapi/fixtures/test.json

# echo "no dumps selected"