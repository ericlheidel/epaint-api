from django.db import models


class PaintType(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
