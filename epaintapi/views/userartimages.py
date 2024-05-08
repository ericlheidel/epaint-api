import base64
from rest_framework import *
from epaintapi.models import *
from rest_framework.permissions import *
from rest_framework.response import *
from rest_framework.status import *
from rest_framework.exceptions import *
from rest_framework.serializers import *
from rest_framework.viewsets import *
from django.core.files.base import ContentFile


class UserArtImageSerializer(ModelSerializer):

    class Meta:
        model = UserArtImage
        fields = (
            "id",
            "user_id",
            "image_path",
        )


class UserArtImages(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):

        new_user_art_image = UserArtImage()
        new_user_art_image.user = request.auth.user

        if "image_path" in request.data:
            format, imgstr = request.data["image_path"].split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'{new_user_art_image.id}-{request.data["user_token"]}.{ext}',
            )

            new_user_art_image.image_path = data

        try:

            new_user_art_image.full_clean()
            new_user_art_image.save()

            serializer = UserArtImageSerializer(
                new_user_art_image, context={"request": request}
            )

            return Response(serializer.data, status=HTTP_201_CREATED)

        except ValidationError as err:
            return Response({"error": err.args[0]}, status=HTTP_400_BAD_REQUEST)
