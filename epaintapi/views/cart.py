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
            open_order = Order.objects.get(user=current_user, payment_type__isnull=True)

        except Order.DoesNotExist:
            open_order = Order()
            open_order.created_date = datetime.datetime.now()
            open_order.user = current_user
            open_order.full_clean()
            open_order.save()
