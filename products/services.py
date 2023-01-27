from typing import Dict

import redis
from django.conf import settings
from redis.exceptions import LockError
from rest_framework import serializers

from orders.serializers import CreateOrderSerializer
from shops.models import Shop
from users.models import Address, Customer

from .models import ProductVariant

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def buy_product(
    product_variant: ProductVariant,
    quantity: int,
    user: Customer,
    address: Address,
    shop: Shop,
    payment: str,
) -> Dict:
    """
    Buy product service function
    """

    # lock product variant quantity field
    lock = r.lock(f"product_variant_{product_variant.id}_quantity", timeout=1)
    try:
        if lock.acquire():
            if type(quantity) != int:
                try:
                    quantity = int(quantity)
                except ValueError:
                    raise serializers.ValidationError("Invalid quantity")
            if product_variant.stock < quantity:
                raise serializers.ValidationError("Not enough quantity")
            product_variant.stock -= quantity
            product_variant.save()
            order_item = CreateOrderSerializer(
                data={
                    "payment": payment,
                    "product_variant": product_variant.id,
                    "quantity": quantity,
                    "user": user,
                    "address": address,
                    "shop": shop,
                }
            )
            order_item.is_valid(raise_exception=True)
            order_item.save()
            return order_item.data

    except LockError:
        raise serializers.ValidationError("Lock error")
