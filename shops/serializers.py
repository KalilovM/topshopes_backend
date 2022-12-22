from rest_framework import serializers

from users.serializers import CustomerSerializer
from .models import (
    Link,
    Shop,
)


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for Link model
    Return name and link
    """

    class Meta:
        model = Link
        fields = ["name", "link"]


class ShopSerializer(serializers.ModelSerializer):
    """
    Shop serializer
    Return all fields
    """

    id = serializers.ReadOnlyField()
    user = CustomerSerializer()

    class Meta:
        model = Shop
        fields = "__all__"


class SingleShopSerializer(serializers.ModelSerializer):
    from products.serializers import ProductSerializer

    """
    Only single shop serializer
    Return only one shop with all fields
    """

    id = serializers.ReadOnlyField()
    user = CustomerSerializer(read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"
