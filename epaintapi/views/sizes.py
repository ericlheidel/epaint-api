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

    def create(self, request):

        new_size = Size()
        new_size.size = request.data["size"]
        new_size.price = request.data["price"]

        try:
            new_size.full_clean()
            new_size.save()
            serializer = SizeSerializer(new_size, context={"request": request})
            return Response(serializer.data, status=HTTP_201_CREATED)

        except ValidationError as err:
            return Response({"error": err.messages}, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None):

        size = Size.objects.get(pk=pk)

        serializer = SizeSerializer(size, many=False, context={"request": request})

        return Response(serializer.data, status=HTTP_200_OK)
