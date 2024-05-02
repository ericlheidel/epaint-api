from rest_framework.serializers import *
from rest_framework.status import *
from rest_framework.permissions import *
from rest_framework.viewsets import *
from rest_framework.response import *
from django.core.files.base import ContentFile
from epaintapi.models import *
import base64


class UserImageSerializer(ModelSerializer):

    class Meta:
        model = UserImage
        fields = (
            "id",
            "user_id",
            "image_path",
        )
        depth = 1


class UserImages(ViewSet):

    def create(self, request):

        new_user_image = UserImage()

        if "image_path" in request.data:
            format, imgstr = request.data["image"].split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), 
                name=f"{new_user_image.id}-{request.data["name"]}.{ext}")
            
            new_user_image.image_path = data

        try:
            
            new_user_image.full_clean()

            new_user_image.save()

            serializer = UserImageSerializer(new_user_image, context={"request": request})

            return Response(serializer.data, status=HTTP_201_CREATED)
        
        except ValidationError as err:
            return Response({"error": err.args[0]}, status=HTTP_400_BAD_REQUEST)
