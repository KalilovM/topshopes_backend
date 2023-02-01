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
        verbose_name=_("Is Verified"), null=True, blank=True)

    def __str__(self):
        return f"{self.payment_type} {self.phone_number} {self.bank_account}"


class TransferMoney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey("payments.Payment", on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Amount"))
    shop = models.ForeignKey("shops.Shop", on_delete=models.CASCADE)
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Tax"))
    confirm_photo = models.ImageField(
        upload_to=PathAndRename("payment/transfer/confirm_photo"), blank=True, null=True)

    def __str__(self):
        return f"{self.payment} {self.amount}"

    def save(self, *args, **kwargs):
        a = 0
        b = 0
        for i in self.payment.orders.all():
            a += i.product_variant.tax_price * i.quantity
            b += i.product_variant.overall_price * i.quantity
        self. amount = b
        self.tax = a
        super().save(*args, **kwargs)
        

