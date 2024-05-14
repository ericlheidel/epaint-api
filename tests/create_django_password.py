from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase


class CreateDjangoPassword(APITestCase):

    def test_create_django_password_bob(self):

        password = "ThisIsMyPassword1234554321!!"

        django_password = make_password(password)

        print(f"pw = {django_password}")
