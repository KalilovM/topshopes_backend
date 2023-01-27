from django.db import models
from core.helpers import PathAndRename
import uuid
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    TYPES = (
        ("elsom", "Elsom"),
        ("visa", "Visa"),
        ("o_dengi", "O'Dengi"),
        ("balance", "Balance"),
        ("mbank", "Mbank"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_type = models.CharField(
        max_length=20, choices=TYPES, verbose_name=_("Payment Type")
    )
    confirm_photo = models.ImageField(
        PathAndRename("payment/confirm_photo"),
    )
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    bank_account = models.CharField(max_length=20, verbose_name=_("Bank Account"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))
