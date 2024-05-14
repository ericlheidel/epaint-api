import json
import datetime
from rest_framework.status import *
from rest_framework.test import APITestCase


class CartTests(APITestCase):
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
        data = {
            "name": "name",
        }
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

        # Create a size
        url = "/sizes"
        data = {
            "size": "400ml",
            "price": 9.99,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(json_response["size"], "400ml")
        self.assertEqual(json_response["price"], 9.99)

    def test_add_paint_to_cart(self):

        # When an order doesn't exist, /cart GET should create an order

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/cart", None, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get order to confirm it was created

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/orders/1", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 1,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "purchase_date": None,
                "user_id": 1,
                "payment_type_id": None,
                "payment": None,
                "is_completed": False,
                "items": [],
                "total": 0,
                "number_of_items": 0,
            },
        )

        data = {
            "paint_id": 1,
            "size_id": 1,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post("/profile/cart", data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get cart to confirm it has a paint in it

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/cart", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 1,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "purchase_date": None,
                "user_id": 1,
                "payment_type_id": None,
                "payment": None,
                "is_completed": False,
                "items": [
                    {
                        "id": 1,
                        "paint": {
                            "id": 1,
                            "color": "color1",
                            "paint_number": "1111",
                            "image_one": None,
                            "image_two": None,
                            "hex": None,
                            "rgb": None,
                            "cmyk": None,
                            "paint_type_id": 1,
                            "paint_type": {"id": 1, "name": "name"},
                        },
                        "size": {"id": 1, "size": "400ml", "price": 9.99},
                    }
                ],
                "total": 9.99,
                "number_of_items": 1,
            },
        )

    def test_delete_paint_from_cart(self):

        # When an order doesn't exist, /cart GET should create an order

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/cart", None, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get order to confirm it was created

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/orders/1", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 1,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "purchase_date": None,
                "user_id": 1,
                "payment_type_id": None,
                "payment": None,
                "is_completed": False,
                "items": [],
                "total": 0,
                "number_of_items": 0,
            },
        )

        data = {
            "paint_id": 1,
            "size_id": 1,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post("/profile/cart", data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get cart to confirm it has a paint in it

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/cart", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 1,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "purchase_date": None,
                "user_id": 1,
                "payment_type_id": None,
                "payment": None,
                "is_completed": False,
                "items": [
                    {
                        "id": 1,
                        "paint": {
                            "id": 1,
                            "color": "color1",
                            "paint_number": "1111",
                            "image_one": None,
                            "image_two": None,
                            "hex": None,
                            "rgb": None,
                            "cmyk": None,
                            "paint_type_id": 1,
                            "paint_type": {"id": 1, "name": "name"},
                        },
                        "size": {"id": 1, "size": "400ml", "price": 9.99},
                    }
                ],
                "total": 9.99,
                "number_of_items": 1,
            },
        )

        # Delete paint from cart (order)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.delete("/cart/1", None, format="json")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
