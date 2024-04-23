from django.core.exceptions import *
from django.http import *
from rest_framework.viewsets import *
from rest_framework.response import *
from django.db.models import Q
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

        search_text = request.query_params.get("search_text", None)
        order_by = request.query_params.get("order_by", None)

        paints = Paint.objects.all()

        if search_text is not None:
            paints = paints.filter(
                Q(color__contains=search_text)
                | Q(paint_number__contains=search_text)
                | Q(hex__contains=search_text)
                | Q(rgb__contains=search_text)
                | Q(cmyk__contains=search_text)
            )

        if order_by is not None:
            paints = paints.order_by(order_by)

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

    #!!! NOT WORKING
    def update(self, request, pk=None):

        paint = Paint.objects.get(pk=pk)

        if "hex" in request.data:
            paint.hex = request.data["hex"]

        if "rgb" in request.data:
            paint.rgb = request.data["rgb"]

        if "cmyk" in request.data:
            paint.cmyk = request.data["cmyk"]

        paint.full_clean()
        paint.save()

        return Response(
            {"message": "Paint successfully update"}, status=status.HTTP_204_NO_CONTENT
        )
