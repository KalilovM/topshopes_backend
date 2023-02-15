import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.models import Order

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
    confirm_photo = models.ImageField(upload_to=PathAndRename("payment/confirm_photo"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    bank_account = models.CharField(max_length=20, verbose_name=_("Bank Account"))
    is_verified = models.BooleanField(
        verbose_name=_("Is Verified"), null=True, blank=True
    )

    def __str__(self):
        return f"{self.payment_type} {self.phone_number} {self.bank_account}"

    def save(self, *args, **kwargs):
        order = Order.objects.get(payment=self)
        if self.is_verified:
            order.status = "paid"
            order.save()
        if self.is_verified is False:
            order.status = "payment_error"
            order.save()
        super().save(*args, **kwargs)


class TransferMoney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(
        "payments.Payment", on_delete=models.CASCADE, related_name="transfer_money"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount")
    )
    shop = models.ForeignKey("shops.Shop", on_delete=models.CASCADE)
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Tax"))
    confirm_photo = models.ImageField(
        upload_to=PathAndRename("payment/transfer/confirm_photo"), blank=True, null=True
    )

    def __str__(self):
        return f"{self.payment} {self.amount}"
