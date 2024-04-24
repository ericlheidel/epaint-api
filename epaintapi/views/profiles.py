from django.contrib.auth.models import User
from rest_framework import serializers, status
from django.http import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import *
from rest_framework.viewsets import *
from epaintapi.models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        depth = 1


class UserInfoSerializer(serializers.ModelSerializer):

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

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return HttpResponseBadRequest(ex)
