import datetime
from rest_framework.viewsets import *
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.exceptions import *
from django.contrib.auth.models import User
from epaintapi.models import *


class Cart(ViewSet):

    def create(self, request):

        try:
            open_order = Order.objects.get(
                user=request.auth.user, payment_type__isnull=True
            )

        except Order.DoesNotExist:
            open_order = Order()
            open_order.created_date = datetime.datetime.now()
            open_order.user = request.auth.user
            open_order.payment_type = None
            open_order.full_clean()
            open_order.save()

        return Response({}, status=HTTP_204_NO_CONTENT)
