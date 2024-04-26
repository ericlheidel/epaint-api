from django.core.exceptions import *
from django.http import *
from rest_framework.viewsets import *
from rest_framework.response import *
from rest_framework.permissions import *
from rest_framework.serializers import *
from rest_framework.status import *
from epaintapi.models import *


class SizeSerializer(ModelSerializer):

    class Meta:
        model = Size
        fields = (
            "id",
            "size",
            "price",
        )


class Sizes(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):

        sizes = Size.objects.all()

        serializer = SizeSerializer(sizes, many=True, context={"request": request})

        return Response(serializer.data, status=HTTP_200_OK)
