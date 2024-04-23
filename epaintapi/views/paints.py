from django.core.exceptions import *
from django.http import *
from rest_framework.viewsets import *
from rest_framework.response import *
import base64
from rest_framework import serializers, status
from rest_framework.permissions import *
from epaintapi.models import Paint


class PaintSerializer(serializers.ModelSerializer):
    """JSON Serializer for Paints"""

    class Meta:
        model = Paint
        fields = (
            "id",
            "color",
            "paint_number",
            "image_one",
            "image_two",
            "hex",
            "rgb",
            "cmyk",
            "paint_type_id",
        )


class Paints(ViewSet):
    """Request handlers for Paints"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):

        paints = Paint.objects.all()

        try:

            serializer = PaintSerializer(
                paints, many=True, context={"request": request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):

        try:
            paint = Paint.objects.get(pk=pk)

            serializer = PaintSerializer(
                paint, many=False, context={"request": request}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Paint.DoesNotExist:

            return Response(
                {"message": "The requested Paint does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return HttpResponseServerError(ex)
