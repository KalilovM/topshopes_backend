from shops.mixins import ShopRelatedField
from users.mixins import CustomerRelatedField
from .models import OrderItem, Order
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
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
    user = CustomerRelatedField()
    shop = ShopRelatedField()
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
