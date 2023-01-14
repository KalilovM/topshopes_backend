from typing import Dict

from rest_framework import serializers

from orders.serializers import CreateOrderSerializer
from shops.models import Shop
from users.models import Address, Customer
from .models import ProductVariant


def buy_product(
        product_variant: ProductVariant,
        quantity: int,
        user: Customer,
        address: Address,
        shop: Shop,
) -> Dict:
    """
    Buy product service function
    """
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
