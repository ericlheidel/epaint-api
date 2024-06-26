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


class OrderPaymentSerializer(ModelSerializer):

    the_last_four_numbers = SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "name",
            "the_last_four_numbers",
        )

    def get_the_last_four_numbers(self, obj):
        return obj.acct_number[-4:]


class OrderSerializer(ModelSerializer):

    items = OrderPaintSerializer(many=True)
    total = SerializerMethodField()
    number_of_items = SerializerMethodField()
    is_completed = SerializerMethodField()
    payment = OrderPaymentSerializer(many=False, source="payment_type")

    class Meta:
        model = Order
        fields = (
            "id",
            "created_date",
            "purchase_date",
            "user_id",
            "payment_type_id",
            "payment",
            "is_completed",
            "items",
            "total",
            "number_of_items",
        )

    def get_total(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.size.price
        return round(total, 2)

    def get_number_of_items(self, obj):
        items = obj.items.all()
        number_of_items = len(items)
        return number_of_items

    def get_is_completed(self, obj):
        return obj.payment_type_id is not None


class Orders(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            order = Order.objects.get(pk=pk, user=request.auth.user)
            serializer = OrderSerializer(order, context={"request": request})
            return Response(serializer.data)

        except Order.DoesNotExist:
            return Response(
                {
                    "message": "The requested order does not exist, or you do not have permission to access it."
                },
                status=HTTP_404_NOT_FOUND,
            )

    def list(self, request):

        try:
            orders = Order.objects.filter(user=request.auth.user)

            closed = self.request.query_params.get("closed")

            if closed == "true":
                orders = Order.objects.filter(
                    user=request.auth.user, payment_type_id__isnull=False
                )

            if closed == "false":
                orders = Order.objects.filter(
                    user=request.auth.user, payment_type_id__isnull=True
                )

            serializer = OrderSerializer(
                orders, many=True, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_200_OK)

        except Order.DoesNotExist as err:
            return Response({"message": err.args[0]}, HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):

        try:

            order = Order.objects.get(user=request.auth.user, pk=pk)
            order.payment_type_id = request.data["payment_type_id"]
            order.purchase_date = request.data["purchase_date"]
            order.save()

            return Response({}, status=HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as err:
            return Response({"message": err.args[0]}, status=HTTP_404_NOT_FOUND)
