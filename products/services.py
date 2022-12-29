from django.core.exceptions import ValidationError
from django.db import transaction
from .models import ProductVariant
from orders.models import OrderItem, Order


def buy_product(
    product_variant: ProductVariant, quantity: int, order_id: Order
) -> OrderItem:
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
        order_item = OrderItem.objects.create(
            product_variant=product_variant,
            product_quantity=quantity,
            product_price=product_variant.price,
            order=order_id,
        )
        # return order
        return order_item
