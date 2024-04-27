import datetime
from django.http import *
from rest_framework.viewsets import *
from rest_framework.serializers import *
from rest_framework.status import *
from rest_framework.response import *
from .paints import PaintSerializer
from .sizes import SizeSerializer
from epaintapi.models import *
from django.contrib.auth.models import User


class OrderPaintSerializer(ModelSerializer):

    paint = PaintSerializer(many=False)
    size = SizeSerializer(many=False)

    class Meta:
        model = OrderPaint
        fields = (
            "id",
            "paint",
            "size",
        )
        depth = 1


class OrderSerializer(ModelSerializer):

    items = OrderPaintSerializer(many=True)
    total = SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "created_date",
            "user_id",
            "payment_type_id",
            "items",
            "total",
        )

    def get_total(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.size.price
        return total


class Orders(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            order = Order.objects.get(pk=pk, user=request.auth.user)
            serializer = OrderSerializer(order, context={"request": request})
            return Response(serializer.data)

        except Order.DoesNotExist as ex:
            return Response(
                {
                    "message": "The requested order does not exist, or you do not have permission to access it."
                },
                status=HTTP_404_NOT_FOUND,
            )

    # This is for Testing Purposes Only
    # def create(self, request):

    #     new_order = Order()
    #     new_order.created_date = datetime.datetime.now
    #     new_order.user_id = request.auth.user
    #     new_order.payment_type = None
