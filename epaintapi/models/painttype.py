from django.db.models import *


class PaintType(Model):

    name = CharField(max_length=255, null=False, blank=False)
