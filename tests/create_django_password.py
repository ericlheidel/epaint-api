from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase


class CreateDjangoPassword(APITestCase):

    def test_create_django_password_bob(self):

        password = "bob"

        django_password = make_password(password)

        print(f"bob = {django_password}")

    def test_create_django_password_tim(self):

        password = "tim"

        django_password = make_password(password)

        print(f"tim = {django_password}")

    def test_create_django_password_tom(self):

        password = "tom"

        django_password = make_password(password)

        print(f"tom = {django_password}")
