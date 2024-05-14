from django.db.models import *
from django.contrib.auth.models import User


class UserInfo(Model):

    user = OneToOneField(
        User,
        on_delete=DO_NOTHING,
    )

    address = CharField(max_length=500)

    phone_number = CharField(max_length=15)
