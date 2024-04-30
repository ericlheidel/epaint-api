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

    def test_create_payment_type(self):

        url = "/payments"

        data = {
            "name": "Visa",
            "acct_number": "1234-5678-8765-4321",
            "ex_date": "2030-03-03",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
