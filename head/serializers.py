from rest_framework import serializers

from products.models import Brand, Category, Product
from products.serializers import ProductVariantSerializer
from shops.models import Shop
from users.models import Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "tax"]


class AdminShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name"]


class AdminBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "image"]


class AdminCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class AdminProductSerializer(serializers.ModelSerializer):
    """
    Product serializer for read only
    Return necessary fields for list view
    """

    brand = AdminBrandSerializer(read_only=True)
    shop = AdminShopSerializer(read_only=True)
    variants = ProductVariantSerializer(read_only=True, many=True)
    category = AdminCategoryReadSerializer(read_only=True)
    thumbnail = serializers.URLField(read_only=True)
    discount = serializers.IntegerField()
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    overall_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "shop",
            "description",
            "name",
            "brand",
            "rating",
            "category",
            "unit",
            "variants",
            "thumbnail",
            "discount",
            "discount_price",
            "overall_price",
            "price",
        ]


class AdminCustomerSerializer(serializers.ModelSerializer):
    """
    Serializer Customer for admin only
    """
    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "is_superuser",
            "is_seller"
        ]
