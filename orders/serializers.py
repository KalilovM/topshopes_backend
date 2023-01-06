from rest_framework import serializers
from .models import Order
from shops.serializers import ShopSerializer
from users.serializers import CustomerSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for read only
    """

    user = CustomerSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    shop = ShopSerializer(read_only=True)

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

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        super().create(validated_data)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
