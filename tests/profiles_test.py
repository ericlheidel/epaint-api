import json
from rest_framework.status import *
from rest_framework.test import APITestCase


# Tests include:
# list (which only gets the profile of the Authenticated user)


class ProfileTests(APITestCase):
    def setUp(self) -> None:

        # Create a User
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

    def test_get_profile(self):

        url = "/profile"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json_response["address"], "212 Broadway")
        self.assertEqual(json_response["phone_number"], "423-555-1234")
        self.assertEqual(json_response["user_id"], 1)

        expected_user = {
            "username": "eric",
            "first_name": "Eric",
            "last_name": "Heidel",
            "email": "eric@ericheidel.com",
        }

        self.assertEqual(json_response["user"], expected_user)
