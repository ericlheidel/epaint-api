from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from django.db import models
from .painttype import PaintType


class Paint(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    color = models.CharField(max_length=255, null=False, blank=False)

    paint_number = models.CharField(max_length=12, null=False, blank=False)

    image_one = models.ImageField(
        upload_to="media",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )

    image_two = models.ImageField(
        upload_to="media",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )

    hex = models.CharField(max_length=7, null=True, blank=True)

    rgb = models.CharField(max_length=12, null=True, blank=True)

    cmyk = models.CharField(max_length=12, null=True, blank=True)

    paint_type = models.ForeignKey(
        PaintType, on_delete=models.DO_NOTHING, related_name="paints"
    )
