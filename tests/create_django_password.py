from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase


class CreateDjangoPassword(APITestCase):

    def test_create_django_password(self):

        password = "tom"

        django_password = make_password(password)

        print(django_password)
