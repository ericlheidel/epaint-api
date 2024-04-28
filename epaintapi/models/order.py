from django.db.models import *
from django.contrib.auth.models import User
from .payment import Payment


class Order(Model):

    user = ForeignKey(User, on_delete=DO_NOTHING, related_name="order")

    created_date = DateField(default="0000-00-00")

    payment_type = ForeignKey(
        Payment, on_delete=DO_NOTHING, null=True, blank=True, related_name="orders"
    )
