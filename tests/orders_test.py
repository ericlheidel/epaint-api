import json
import datetime
from rest_framework.status import *
from rest_framework.test import APITestCase
from epaintapi.models import *


class OrderTests(APITestCase):
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

        # Create a paint type
        url = "/painttypes"
        data = {"name": "name"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "name")

        # Create a paint with the created paint type
        url = "/paints"
        data = {
            "color": "color1",
            "paint_number": "1111",
            "paint_type_id": 1,
            "hex": None,
            "rgb": None,
            "cmyk": None,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json_response["color"], "color1")
        self.assertEqual(json_response["paint_number"], "1111")
        self.assertEqual(json_response["paint_type_id"], 1)
        self.assertEqual(json_response["hex"], None)
        self.assertEqual(json_response["rgb"], None)
        self.assertEqual(json_response["cmyk"], None)
