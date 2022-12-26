from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import Field

from products.models import Product
from shops.models import Shop
from shops.serializers import ShopSerializer
from users.serializers import Customer, CustomerSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer get only product's id and order
    Returns all information
    """

    product_image = serializers.ReadOnlyField()
    product_name = serializers.ReadOnlyField()
    product_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "product_image",
            "product_name",
            "product_price",
            "product_quantity",
        ]

    @atomic
    def create(self, validated_data):
        """
        Getting data form product and fill other fields
        """
        product = Product.objects.get(id=validated_data["product"])
        validated_data["product_image"] = product.thumbnail
        validated_data["product_name"] = product.title
        validated_data["product_price"] = product.price
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

    user = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    shop: Field = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Shop.objects.all()
    )
    items: Field = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=OrderItem.objects.all()
    )

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

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        super().create(validated_data)
