import uuid
from django.db import models
from core.helpers import PathAndRename


class OrderItem(models.Model):
    product_image = models.ImageField(upload_to=PathAndRename("orders/items/product/"))
    product_name = models.CharField(max_length=100)
    product_price = models.PositiveIntegerField()
    product_quantity = models.PositiveIntegerField()
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.product_name


class Order(models.Model):
    STATUSES = (
        ("PENDING", "Pending"),
        ("PROCCESSING", "Proccessing"),
        ("DELIVERED", "Delivered"),
        ("CENCELLED", "Cencelled"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    tax = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveSmallIntegerField()
    total_price = models.PositiveIntegerField()
    is_delivered = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=35, choices=STATUSES)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name
