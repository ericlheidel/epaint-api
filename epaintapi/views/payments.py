import datetime
from rest_framework.serializers import *
from rest_framework.viewsets import *
from rest_framework.permissions import *
from rest_framework.response import *
from rest_framework.status import *

from epaintapi.models import *
from .profiles import UserInfoSerializer


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment()
        fields = (
            "id",
            "name",
            "acct_number",
            "ex_date",
            "created_date",
            "user",
        )


class Payments(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):

        new_payment = Payment()
        new_payment.name = request.data["name"]
        new_payment.acct_number = request.data["acct_number"]
        new_payment.ex_date = request.data["ex_date"]
        new_payment.created_date = datetime.datetime.now()
        new_payment.user = request.auth.user
        new_payment.full_clean()
        new_payment.save()

        serializer = PaymentSerializer(new_payment, context={"request": request})

        return Response(serializer.data, status=HTTP_201_CREATED)
