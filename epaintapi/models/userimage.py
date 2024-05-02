from django.db.models import *
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class UserImage(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    user = OneToOneField(User, on_delete=DO_NOTHING)

    image_path = ImageField(
        upload_to="userimages",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )
