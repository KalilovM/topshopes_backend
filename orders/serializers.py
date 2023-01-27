from rest_framework import serializers

from payments.models import Payment
from products.serializers import ProductSerializer, ProductVariantSerializer
from shops.serializers import ShopSerializer
from users.serializers import AddressSerializer, CustomerSerializer

from .models import Order


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
            "address",
            "payment",
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for create only
    """

    class Meta:
        model = Order
        fields = ["shop", "user", "product_variant", "quantity", "address", "payment"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def validate_payment(self, value):
        payment = Payment.objects.get(id=value).orders.shop
        if payment.shop != self.initial_data["shop"]:
            raise serializers.ValidationError("Order and payment shop must be the same")
