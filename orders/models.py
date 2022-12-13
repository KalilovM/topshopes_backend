from decimal import Decimal
from typing import Tuple, Dict
import uuid
from django.db import models
from core.helpers import PathAndRename


class OrderItem(models.Model):
    """
    Model of item for order
    Contains one product information
    """

    product_image = models.ImageField(upload_to=PathAndRename("orders/items/product/"))
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.PositiveIntegerField()
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.product_name

    def change_order_total(self, isAdd: bool) -> None:
        total_price = self.product_price * Decimal(self.product_quantity)
        order = Order.objects.get(id=self.order.id)
        total_price -= total_price * Decimal(order.discount) / 100

        if isAdd:
            order.total_price += total_price
        else:
            order.total_price -= total_price
        order.total_price += total_price * Decimal(order.tax) / 100

        order.save()

    def save(self, *args, **kwargs) -> None:
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
        ("PROCCESSING", "Proccessing"),
        ("DELIVERED", "Delivered"),
        ("CENCELLED", "Cencelled"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        "users.Customer",
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey("shops.Shop", on_delete=models.CASCADE)
    tax = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(
        max_digits=15, decimal_places=2, editable=True, default=0
    )
    is_delivered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=35, choices=STATUSES, default="PENDING")
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
