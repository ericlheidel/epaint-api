from django.db.models import *
from django.contrib.auth.models import User


class UserArtImage(Model):

    user = ForeignKey(User, on_delete=CASCADE, related_name="images")

    image_path = ImageField(
        upload_to="userartimages",
        height_field=None,
        width_field=None,
        max_length=None,
        null=False,
        blank=False,
    )
