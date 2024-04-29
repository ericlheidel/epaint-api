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

        item = OrderPaint()
        item.product = Paint.objects.get(pk=request.data["paint_id"])
        item.order = open_order
        item.full_clean()
        item.save()

        return Response({}, status=HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            order = Order.objects.get(user=request.auth.user, payment_type=None)
            order_paint = OrderPaint.objects.get(pk=pk, order=order)
            order_paint.delete()

            return Response({}, status=HTTP_204_NO_CONTENT)

        except OrderPaint.DoesNotExist as err:
            return Response({"message": err.args[0]}, status=HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response({}, status=HTTP_500_INTERNAL_SERVER_ERROR)
