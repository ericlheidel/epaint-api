from django.db.models import *
from django.core.validators import MaxValueValidator, MinValueValidator


class Size(Model):

    size = CharField(max_length=255, null=False, blank=False)

    price = FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])
