from django.core.exceptions import *
from django.core.files.base import *
from django.http import *
from rest_framework.viewsets import *
from rest_framework.response import *
from django.db.models import Q
import base64
from rest_framework.permissions import *
from rest_framework.serializers import *
from rest_framework.status import *
from epaintapi.models import *
from .painttypes import PaintTypeSerializer


class PaintSerializer(ModelSerializer):
    """JSON Serializer for Paints"""

    paint_type = PaintTypeSerializer(many=False)

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
            "paint_type",
        )


class Paints(ViewSet):
    """Request handlers for Paints"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):

        search_text = request.query_params.get("search_text", None)
        order_by = request.query_params.get("order_by", None)
        paint_type_id = request.query_params.get("paint_type_id", None)

        paints = Paint.objects.all()

        if search_text is not None:
            paints = paints.filter(
                Q(color__contains=search_text)
                | Q(paint_number__contains=search_text)
                | Q(hex__contains=search_text)
                | Q(rgb__contains=search_text)
                | Q(cmyk__contains=search_text)
            )

        if order_by:
            paints = paints.order_by(order_by)

        if paint_type_id:
            paints = paints.filter(paint_type__id=paint_type_id)

        try:

            serializer = PaintSerializer(
                paints, many=True, context={"request": request}
            )

            return Response(serializer.data, status=HTTP_200_OK)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):

        try:
            paint = Paint.objects.get(pk=pk)
            serializer = PaintSerializer(
                paint, many=False, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_200_OK)

        except Paint.DoesNotExist:
            return Response(
                {"message": "The requested Paint does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return HttpResponseServerError(ex)

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
            {"message": "Paint successfully update"}, status=HTTP_204_NO_CONTENT
        )

    def create(self, request):
        new_paint = Paint()
        new_paint.color = request.data["color"]
        new_paint.paint_number = request.data["paint_number"]
        new_paint.hex = request.data["hex"]
        new_paint.rgb = request.data["rgb"]
        new_paint.cmyk = request.data["cmyk"]
        new_paint.paint_type_id = request.data["paint_type_id"]

        if "image_one" in request.data:
            format, imgstr = request.data["image_one"].split(";base64")
            ext = format.split("?")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'{new_paint.id}-{request.data["name"]}.{ext}',
            )

            new_paint.image_one = data

        if "image_two" in request.data:
            format, imgstr = request.data["image_two"].split(";base64")
            ext = format.split("?")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'{new_paint.id}-{request.data["name"]}.{ext}',
            )

            new_paint.image_two = data

        try:
            new_paint.full_clean()

            new_paint.save()

            serializer = PaintSerializer(new_paint, context={"request": request})

            return Response(serializer.data, status=HTTP_201_CREATED)

        except ValidationError as err:
            return Response({"error": err.message}, status=HTTP_400_BAD_REQUEST)
