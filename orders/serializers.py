from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import Field

from products.models import ProductVariant
from shops.models import Shop
from shops.serializers import ShopSerializer
from users.serializers import Customer, CustomerSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer get only product's id and order
    Returns all information
    """

    class Meta:
        model = OrderItem
        fields = [
            "product_image",
            "product_name",
            "product_price",
            "product_quantity",
            "product_variant",
            "order",
        ]

    @atomic
    def create(self, validated_data):
        """
        Getting data form product and fill other fields
        """
        product_variant = ProductVariant.objects.get(
            id=validated_data["product_variant"]
        )
        validated_data["product_image"] = product_variant.thumbnail
        validated_data["product_name"] = product_variant.product.title
        validated_data["product_price"] = product_variant.price
        super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for read only
    """

    user = CustomerSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    shop = ShopSerializer(read_only=True)
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


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for create only
    """

    class Meta:
        model = Order
        fields = [
            "id",
            "shop",
            "tax",
            "created_at",
            "discount",
            "is_delivered",
            "shipping_address",
            "status",
            "delivered_at",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        super().create(validated_data)
