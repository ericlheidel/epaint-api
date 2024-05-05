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

        # Create a payment

        url = "/payments"

        data = {
            "name": "Visa",
            "acct_number": "1234-5678-8765-4321",
            "ex_date": "2030-03-03",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_create_an_order_via_cart_viewset(self):

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

    def test_create_an_order_via_the_profile_viewset(self):

        url_one = "/profile/cart"
        data = {
            "paint_id": 1,
            "size_id": 1,
        }

        # When an order doesn't exist, /profile/cart to add
        # a paint to the order should create an order

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url_one, data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_get_one_order(self):

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

    def test_update_order_with_payment(self):

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

        # Update order with a payment (this closes an order)

        data = {
            "payment_type_id": 1,
            "purchase_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put("/orders/1", data, format="json")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # Get the order to confirm that payment_type_id is not null

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/orders/1", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 1,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "purchase_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "user_id": 1,
                "payment_type_id": 1,
                "payment": {
                    "name": "Visa",
                    "the_last_four_numbers": "4321",
                },
                "is_completed": True,
                "items": [],
                "total": 0,
                "number_of_items": 0,
            },
        )

    def test_get_all_orders(self):

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

        # Update order with a payment (this closes an order)

        data = {
            "payment_type_id": 1,
            "purchase_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put("/orders/1", data, format="json")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # Get the order to confirm that payment_type_id is not null

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/orders/1", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 1,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "purchase_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "user_id": 1,
                "payment_type_id": 1,
                "payment": {
                    "name": "Visa",
                    "the_last_four_numbers": "4321",
                },
                "is_completed": True,
                "items": [],
                "total": 0,
                "number_of_items": 0,
            },
        )

        #     # When an order doesn't exist, /cart GET should create an order

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/cart", None, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get order to confirm it was created

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/orders/2", None, format="json")
        json_response = json.loads(response.content)
        self.assertDictEqual(
            json_response,
            {
                "id": 2,
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

        # Get the two orders to confirm they exist

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get("/orders", None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 2)
