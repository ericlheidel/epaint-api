import datetime
from rest_framework.viewsets import *
from rest_framework.response import *
from rest_framework.status import *
from django.contrib.auth.models import User
from epaintapi.models import *


class Cart(ViewSet):

    def create(self, request):

        current_user = User.objects.get(user=request.auth.user)

        try:
            create_order = Order.objects.get(
                user=current_user, payment_type__isnull=True
            )

        except Order.DoesNotExist:
            create_order = Order()
            create_order.created_date = datetime.datetime.now()
            create_order.user = current_user
            create_order.full_clean()
            create_order.save()
