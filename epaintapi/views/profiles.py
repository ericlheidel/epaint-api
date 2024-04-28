from django.contrib.auth.models import User
from django.http import *
from rest_framework.viewsets import *
from rest_framework.serializers import *
from rest_framework.permissions import *
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.decorators import *
from epaintapi.models import *
from .orders import OrderPaintSerializer, OrderSerializer


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

        if request.method == "GET":

            try:
                open_order = Order.objects.get(
                    user=request.auth.user, payment_type=None
                )
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

            except Order.DoesNotExist as ex:
                return Response({"message": ex.args[0]}, status=HTTP_404_NOT_FOUND)
