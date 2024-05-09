from django.db.models import *
from django.contrib.auth.models import User


class UserImage(Model):

    user = OneToOneField(User, on_delete=CASCADE)

    image_path = ImageField(
        upload_to="userimages",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )
