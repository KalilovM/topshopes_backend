from rest_framework import serializers

from products.models import Brand, Category, Color, Product, ProductVariant, Size
from products.serializers import ImageSerializer, ProductVariantSerializer
from shops.models import Shop


class AdminShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name"]


class AdminBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "image"]


class AdminProductSerializer(serializers.ModelSerializer):
    """
    Product serialzier for read only
    Return necessary fields for list view
    """

    brand = AdminBrandSerializer(read_only=True)
    shop = AdminShopSerializer(read_only=True)
    variants = ProductVariantSerializer(read_only=True, many=True)

    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "shop",
            "title",
            "brand",
            "rating",
            "unit",
            "published",
            "variants",
        ]
