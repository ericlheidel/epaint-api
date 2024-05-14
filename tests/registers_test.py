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

    def test_cant_register_existing_email(self):

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

        # Attempt to create a new user with the same email as the created user

        url = "/register"
        data = {
            "username": "eric_number_2",
            "password": "eric_number_2",
            "email": "eric@ericheidel.com",
            "address": "212 Different Road",
            "phone_number": "555-555-5555",
            "first_name": "Eric Number 2",
            "last_name": "Heidel Number 2",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response["message"], "Email already exists")

    def test_cant_register_user_existing_username(self):

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

        # Attempt to create a new user with the same username as the created user

        url = "/register"
        data = {
            "username": "eric",
            "password": "eric_number_2",
            "email": "eric@ericheidel_number_2.com",
            "address": "212 Different Road",
            "phone_number": "555-555-5555",
            "first_name": "Eric Number 2",
            "last_name": "Heidel Number 2",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(json_response["message"], "Username already exists")
