from core.mixins import CommonRelatedField
from shops.models import Shop
from shops.serializers import ShopSerializer
from users.models import Customer
from users.serializers import CustomerSerializer
from .models import OrderItem, Order
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer to return product information and order id
    """

    class Meta:
        model = OrderItem
        fields = [
            "product_image",
            "product_name",
            "product_price",
            "product_quantity",
            "order",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer to return all order information
    """

    user = CommonRelatedField(
        model=Customer, serializer=CustomerSerializer, read_only=True
    )
    total_price = serializers.ReadOnlyField()
    shop = CommonRelatedField(model=Shop, serializer=ShopSerializer)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shop",
            "items",
            "tax",
            "created_at",
            "discount",
            "total_price",
            "is_delivered",
            "shipping_address",
            "status",
            "delivered_at",
        ]
