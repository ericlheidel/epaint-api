import datetime
from django.contrib.auth.models import User
from django.http import *
from rest_framework.viewsets import *
from rest_framework.serializers import *
from rest_framework.permissions import *
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.decorators import *
from epaintapi.models import *
from .orders import OrderPaintSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )
        depth = 1


class UserInfoSerializer(ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = UserInfo
        fields = (
            "id",
            "address",
            "phone_number",
            "user_id",
            "user",
        )
        depth = 1


class Profiles(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):

        try:
            current_user_info = UserInfo.objects.get(user=request.auth.user)

            serializer = UserInfoSerializer(
                current_user_info, many=False, context={"request": request}
            )

            return Response(serializer.data, status=HTTP_200_OK)

        except Exception as ex:
            return HttpResponseBadRequest(ex)

    @action(methods=["get", "post", "delete"], detail=False)
    def cart(self, request):
        """Shopping Cart Manipulation"""

        """The POST method will add a paint to the cart"""
        """If an order does not exist when a paint is added to the cart,"""
        """This will create an order, therefore creating a cart, and add the paint to the order"""
        if request.method == "POST":

            try:
                open_order = Order.objects.get(
                    user=request.auth.user, payment_type=None
                )

            except Order.DoesNotExist:
                open_order = Order()
                open_order.created_date = datetime.datetime.now()
                open_order.purchase_date = None
                open_order.payment_type = None

                open_order.user = request.auth.user
                open_order.full_clean()
                open_order.save()

            order_paint = OrderPaint()
            order_paint.order = open_order
            order_paint.paint = Paint.objects.get(pk=request.data["paint_id"])
            order_paint.size = Size.objects.get(pk=request.data["size_id"])
            order_paint.full_clean()
            order_paint.save()

            order_paint_json = OrderPaintSerializer(
                order_paint, many=False, context={"request": request}
            )

            return Response(order_paint_json.data, HTTP_201_CREATED)

        return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)
