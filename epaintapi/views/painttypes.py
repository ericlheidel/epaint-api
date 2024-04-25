from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from epaintapi.models import *


class PaintTypeSerializer(ModelSerializer):

    class Meta:
        model = PaintType
        fields = (
            "id",
            "name",
        )


class PaintTypes(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):

        paint_types = PaintType.objects.get(all)

        serializer = PaintTypeSerializer(
            paint_types, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        paint_type = PaintType.objects.get(pk=pk)

        serializer = PaintTypeSerializer(
            paint_type, many=False, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
