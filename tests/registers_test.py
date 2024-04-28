import json
from rest_framework.test import APITestCase
from rest_framework.status import *


# Tests include:
# Register a user


class RegistersTests(APITestCase):
    def test_register_user(self):

        # Create a user
        url = "/register"
        data = {
            "username": "eric",
            "password": "eric",
            "email": "eric@ericheidel.com",
            "address": "212 Broadway",
            "phone_number": "423-555-1234",
            "first_name": "Eric",
            "last_name": "Heidel",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_login_user(self):

        # Create a user
        url = "/register"
        data = {
            "username": "eric",
            "password": "eric",
            "email": "eric@ericheidel.com",
            "address": "212 Broadway",
            "phone_number": "423-555-1234",
            "first_name": "Eric",
            "last_name": "Heidel",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Login created user
        url = "/login"
        data = {
            "username": "eric",
            "password": "eric",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(json_response["valid"], True)
        self.assertIsNotNone(json_response["token"])
        self.assertIsNotNone(json_response["id"])
