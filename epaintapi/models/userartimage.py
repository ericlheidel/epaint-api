from django.db.models import *
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class UserArtImage(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    user = ForeignKey(User, on_delete=DO_NOTHING, related_name="images")

    image_path = ImageField(
        upload_to="userartimages",
        height_field=None,
        width_field=None,
        max_length=None,
        null=False,
        blank=False,
    )
