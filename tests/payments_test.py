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

        # Create payment

        url = "/payments"

        data = {
            "name": "Visa",
            "acct_number": "1234-5678-8765-4321",
            "ex_date": "2030-03-03",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_get_user_payments(self):

        # Create a 2nd payment

        url = "/payments"

        data = {
            "name": "Visa",
            "acct_number": "1234-5678-8765-4321",
            "ex_date": "2030-03-03",
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Get both created payments connected to the created user

        url = "/payments"

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(json_response), 2)


# ++  /$$$$$$$  /$$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$$ /$$   /$$
# ++ | $$__  $$| $$__  $$ /$$__  $$| $$  /$$/| $$_____/| $$$ | $$
# ++ | $$  \ $$| $$  \ $$| $$  \ $$| $$ /$$/ | $$      | $$$$| $$
# ++ | $$$$$$$ | $$$$$$$/| $$  | $$| $$$$$/  | $$$$$   | $$ $$ $$
# ++ | $$__  $$| $$__  $$| $$  | $$| $$  $$  | $$__/   | $$  $$$$
# ++ | $$  \ $$| $$  \ $$| $$  | $$| $$\  $$ | $$      | $$\  $$$
# ++ | $$$$$$$/| $$  | $$|  $$$$$$/| $$ \  $$| $$$$$$$$| $$ \  $$
# ++ |_______/ |__/  |__/ \______/ |__/  \__/|________/|__/  \__/

# def test_update_payment(self):

#     # Update created payment
#     url = "/payments/1"
#     data = {
#         "name": "Discover",
#         "acct_number": "8765-4321-1234-5678",
#         "ex_date": "2050-05-05",
#     }

#     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
#     response = self.client.put(url, data, format="json")
#     self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

#     # Get payment and confirm updates

#     url = "/payments/"

#     response = self.client.get(url, None, format="json")
#     json_response = json.loads(response.content)
#     self.assertEqual(response.status_code, HTTP_200_OK)
#     self.assertEqual(json_response["name"], "Discover")
#     self.assertEqual(json_response["acct_number"], "8765-4321-1234-5678")
#     self.assertEqual(json_response["ex_date"], "2050-05-05")
