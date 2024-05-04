import json
import datetime
from rest_framework.status import *
from rest_framework.test import APITestCase
from epaintapi.models import *


class PaymentTests(APITestCase):
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

    def test_get_all_payment(self):

        # Create a second payment

        url = "/payments"

        data = {
            "name": "Visa",
            "acct_number": "1234-5678-8765-4321",
            "ex_date": "2030-03-03",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        url = "/payments"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(json_response), 2)

    def test_delete_payment_type(self):

        url_one = "/payments/1"
        url_two = "/payments"

        # Delete payment

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.delete(url_one, None, format="json")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # Get payment to confirm it does not exist

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(url_two, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(json_response), 0)

    def test_update_payment(self):

        url_one = "/payments/1"
        url_two = "/payments"
        data = {
            "name": "Discover",
            "acct_number": "8765-4321-1234-5678",
            "ex_date": "2040-04-04",
        }

        # Edit payment

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put(url_one, data, format="json")
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # Get payment to confirm update

        response = self.client.get(url_two, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(json_response["name"], "Discover")
        self.assertEqual(json_response["acct_number"], "8765-4321-1234-5678")
        self.assertEqual(json_response["ex_date"], "2040-04-04")
