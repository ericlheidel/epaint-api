from rest_framework.serializers import *
from rest_framework.status import *
from rest_framework.permissions import *
from rest_framework.viewsets import *
from rest_framework.response import *
from rest_framework.exceptions import *
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

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):

        new_user_image = UserImage()
        new_user_image.user = request.auth.user

        if "image_path" in request.data:

            # Adding encoding to test in Postman
            # file_data = request.data["image_path"].read()
            # imgstr = base64.b64encode(file_data).decode()
            # format, _ = request.data["image_path"].content_type.split("/")

            # This should be the start of the code for use with the front end
            format, imgstr = request.data["image_path"].split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'{new_user_image.id}-{request.data["user_token"]}.{ext}',
            )

            new_user_image.image_path = data

        try:

            new_user_image.full_clean()

            new_user_image.save()

            serializer = UserImageSerializer(
                new_user_image, context={"request": request}
            )

            return Response(serializer.data, status=HTTP_201_CREATED)

        except ValidationError as err:
            return Response({"error": err.args[0]}, status=HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):

        try:

            user_image = UserImage.objects.get(user=request.auth.user)

            serializer = UserImageSerializer(user_image, context={"request": request})

            return Response(serializer.data, status=HTTP_200_OK)

        except UserImage.DoesNotExist as err:
            return Response([], status=HTTP_200_OK)

        except Exception as err:
            return Response(
                {"error": err.args[0]}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):

        try:

            user_image = UserImage.objects.get(pk=pk, user=request.auth.user)
            user_image.delete()

            return Response({}, status=HTTP_204_NO_CONTENT)

        except UserImage.DoesNotExist as err:
            return Response({"message": err.args[0]}, status=HTTP_404_NOT_FOUND)

        except Exception as err:
            return Response(
                {"message": err.args[0]}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )
