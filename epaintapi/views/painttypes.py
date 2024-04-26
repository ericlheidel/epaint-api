from django.core.exceptions import *
from django.http import *
from rest_framework.viewsets import *
from rest_framework.response import *
from rest_framework.serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import *
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

        paint_types = PaintType.objects.all()

        serializer = PaintTypeSerializer(
            paint_types, many=True, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, pk=None):

        try:
            paint_type = PaintType.objects.get(pk=pk)
            serializer = PaintTypeSerializer(
                paint_type, many=False, context={"request": request}
            )
            return Response(serializer.data, status=HTTP_200_OK)

        except PaintType.DoesNotExist:
            return Response(
                {"message": "The requested painttype does not exist"},
                status=HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return HttpResponseServerError(ex)
