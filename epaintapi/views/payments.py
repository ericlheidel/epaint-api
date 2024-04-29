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

    def destroy(elf, request, pk=None):

        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            return Response({}, status=HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as err:
            return Response({"message": err.args[0]}, status=HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(
                {"message": err.args[0]}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):

        try:
            updated_payment = Payment.objects.get(pk=pk)
            updated_payment.name = request.data["name"]
            updated_payment.acct_number = request.data["acct_number"]
            updated_payment.ex_date = request.data["ex_date"]
            updated_payment.full_clean()
            updated_payment.save()

            return Response({}, status=HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as err:
            return Response({"message": err.args[0]}, status=HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(
                {"message": err.args[0]}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )
