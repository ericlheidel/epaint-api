import datetime
from rest_framework.viewsets import *
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.exceptions import *
from django.contrib.auth.models import User
from epaintapi.models import *
from .orders import OrderSerializer, OrderPaintSerializer


class Cart(ViewSet):

    def list(self, request):
        """The GET/list method will get a users cart"""
        """A users cart is an open, unpaid order"""
        """If a user has no open order when the cart is requested,"""
        """TheGET/list method will create an order, therefore creating an empty cart"""

        try:
            open_order = Order.objects.get(user=request.auth.user, payment_type=None)
            items = OrderPaint.objects.filter(order=open_order)
            items_serializer = OrderPaintSerializer(
                items, many=True, context={"request": request}
            )

            order_serializer = OrderSerializer(
                open_order, many=False, context={"request": request}
            )
            order_data = order_serializer.data
            order_data["number_of_items"] = len(items_serializer.data)
            order_data["items"] = items_serializer.data

            return Response(order_data)

        except Order.DoesNotExist:
            open_order = Order()
            open_order.created_date = datetime.datetime.now()
            open_order.user = request.auth.user
            open_order.purchase_date = None
            open_order.payment_type = None
            open_order.full_clean()
            open_order.save()

        return Response({"message": "Order created..."}, status=HTTP_201_CREATED)

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
