from typing import Dict

from django.core.exceptions import ValidationError
from django.db import transaction

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
    # lock the database
    with transaction.atomic():
        # check if product is available
        if product_variant.stock < quantity:
            raise ValidationError("Not enough quantity")
        # update product quantity
        product_variant.stock -= quantity
        product_variant.save()
        # create order
        order_item = CreateOrderSerializer(
            data={
                "product_variant": product_variant,
                "quantity": quantity,
                "user": user,
                "address": address,
                "shop": shop,
            }
        )
        order_item.is_valid(raise_exception=True)
        order_item.save()
        return order_item.data
