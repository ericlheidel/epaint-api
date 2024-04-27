from django.db.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from .order import Order
from .paint import Paint
from .size import Size


class OrderPaint(Model):

    price = FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])

    order = ForeignKey(Order, on_delete=DO_NOTHING, related_name="items")

    paint = ForeignKey(Paint, on_delete=DO_NOTHING, related_name="items")

    size = ForeignKey(Size, on_delete=DO_NOTHING, related_name="items")
