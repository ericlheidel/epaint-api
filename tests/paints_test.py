import json
from rest_framework.status import *
from rest_framework.test import APITestCase


# Tests include:
# list
# retrieve
# update
# create (this is in setUp)


class PaintTests(APITestCase):
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

        # Create a 2nd paint with the created paint type
        url = "/paints"
        data = {
            "color": "color2",
            "paint_number": "2222",
            "paint_type_id": 1,
            "hex": None,
            "rgb": None,
            "cmyk": None,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json_response["color"], "color2")
        self.assertEqual(json_response["paint_number"], "2222")
        self.assertEqual(json_response["paint_type_id"], 1)
        self.assertEqual(json_response["hex"], None)
        self.assertEqual(json_response["rgb"], None)
        self.assertEqual(json_response["cmyk"], None)

    def test_get_all_paints(self):

        url = "/paints"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(json_response), 2)

    def test_get_one_paint(self):

        url = "/paints/1"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json_response["color"], "color1")
        self.assertEqual(json_response["paint_number"], "1111")
        self.assertEqual(json_response["paint_type_id"], 1)
        self.assertEqual(json_response["hex"], None)
        self.assertEqual(json_response["rgb"], None)
        self.assertEqual(json_response["cmyk"], None)

    def test_update_paint(self):

        url = "/paints/1"
        data = {
            "hex": "#000000",
        }

        # Edit the "hex": of a paint
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # Get the paint to confirm the "hex": change
        url = "/paints/1"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json_response["color"], "color1")
        self.assertEqual(json_response["paint_number"], "1111")
        self.assertEqual(json_response["paint_type_id"], 1)
        self.assertEqual(json_response["hex"], "#000000")
        self.assertEqual(json_response["rgb"], None)
        self.assertEqual(json_response["cmyk"], None)
