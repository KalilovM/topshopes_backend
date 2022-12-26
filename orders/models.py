import uuid
from decimal import Decimal
from typing import Dict, Tuple

from django.db import models

from core.helpers import PathAndRename


class OrderItem(models.Model):
    """
    Model of item for order
    Contains one product information
    """

    product_image = models.ImageField(
        upload_to=PathAndRename("orders/items/product/"), blank=True, null=True
    )
    product_name = models.CharField(max_length=100, blank=True, null=True)
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    product_quantity = models.PositiveIntegerField()
    product_variant = models.ForeignKey(
        "products.ProductVariant", on_delete=models.CASCADE, related_name="order_items"
    )
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.product_name

    def fill_product_data(self) -> None:
        self.product_name = self.product_variant.product.title
        self.product_price = self.product_variant.price
        self.product_image = self.product_variant.thumbnail

    def change_order_total(self, is_add: bool) -> None:
        if is_add:
            self.order.total_price += self.product_price * self.product_quantity
        else:
            self.order.total_price -= self.product_price * self.product_quantity
        self.order.save()

    def save(self, *args, **kwargs) -> None:
        self.fill_product_data()
        self.change_order_total(True)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> Tuple[int, Dict[str, int]]:
        self.change_order_total(False)
        return super().delete(*args, **kwargs)


class Order(models.Model):
    """
    Order model to create order for user
    """

    STATUSES = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        "users.Customer",
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey("shops.Shop", on_delete=models.CASCADE)
    tax = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveSmallIntegerField(default=0)
    total_price = models.DecimalField(
        max_digits=15, decimal_places=2, editable=False, default=Decimal(0)
    )
    is_delivered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=35, choices=STATUSES, default="PENDING")
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
