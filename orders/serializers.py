from rest_framework import serializers

from shops.serializers import ShopSerializer
from users.serializers import CustomerSerializer, AddressSerializer
from .models import Order
from products.serializers import ProductVariantSerializer, ProductSerializer



class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for read only
    """

    user = CustomerSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    shop = ShopSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    product = ProductSerializer(read_only=True, source="product_variant.product")
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shop",
            "created_at",
            "total_price",
            "status",
            "delivered_at",
            "product_variant",
            "product",
            "quantity",
            "address"
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for create only
    """

    class Meta:
        model = Order
        fields = [
            "shop",
            "user",
            "product_variant",
            "quantity",
            "address",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
