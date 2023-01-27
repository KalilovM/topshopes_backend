import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.helpers import PathAndRename


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
        upload_to=PathAndRename("payment/confirm_photo"))
    phone_number = models.CharField(
        max_length=20, verbose_name=_("Phone Number"))
    bank_account = models.CharField(
        max_length=20, verbose_name=_("Bank Account"))
    is_verified = models.BooleanField(
        default=False, verbose_name=_("Is Verified"))

    def __str__(self):
        return f"{self.payment_type} {self.phone_number} {self.bank_account}"
