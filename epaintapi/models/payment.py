from django.db.models import *
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel, SOFT_DELETE


class Payment(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE

    name = CharField(max_length=255)

    acct_number = CharField(max_length=255)

    ex_date = DateField(default="0000-00-00")

    created_date = DateField(default="0000-00-00")

    user = ForeignKey(User, on_delete=DO_NOTHING, related_name="payments")
