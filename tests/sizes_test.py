import json
import datetime
from rest_framework.status import *
from rest_framework.test import APITestCase


class SizeTests(APITestCase):
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

        # Create a size
        url = "/sizes"
        data = {"size": "400ml", "price": 9.99}

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json_response["size"], "400ml")
        self.assertEqual(json_response["price"], 9.99)

        # Create a 2nd size
        url = "/sizes"
        data = {"size": "600ml", "price": 14.99}

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json_response["size"], "600ml")
        self.assertEqual(json_response["price"], 14.99)

    def test_get_all_sizes(self):

        url = "/sizes"

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(json_response), 2)

    # def test_get_one_sizes(self):

    #     url = "/sizes/1"

    #     response = self.client.get(url, None, format="json")
    #     json_response = json.loads(response.content)
    #     self.assertEqual(response.status_code, HTTP_200_OK)
    #     self.assertEqual(json_response["size"], "400ml")
    #     self.assertEqual(json_response["price"], 9.99)
