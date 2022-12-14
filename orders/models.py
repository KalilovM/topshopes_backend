import uuid
from decimal import Decimal

from django.db import models


class Order(models.Model):
    """
    Model of order
    Contains one product information
    """

    STATUSES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("delivering", "Delivering"),
        ("delivered", "Delivered"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(
        "users.Customer", on_delete=models.CASCADE, related_name="orders"
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00)
    )
    quantity = models.IntegerField(default=1)
    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="pending")
    address = models.ForeignKey(
        "users.Address", on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.shop}"

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.product_variant.discount_price:
            self.total_price = self.product_variant.discount_price * self.quantity
        self.total_price = self.product_variant.price * self.quantity
        super().save(*args, **kwargs)
