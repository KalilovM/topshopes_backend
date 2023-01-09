from rest_framework import serializers
from rest_framework.serializers import Field

from attributes.serializers import (AttributeSerializer,
                                    AttributeValueSerializer)
from products.models import (Brand, BrandType, Category, Image, Product,
                             ProductVariant)
from reviews.serializers import ReviewSerializer
from shops.models import Shop


class ShopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand serializer able to select fields to represent
    Return all fields
    """

    class Meta:
        model = Brand
        fields = "__all__"


class BrandTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for brand type
    Return all fields
    """

    class Meta:
        model = BrandType
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for product image
    Return only id and image
    """

    class Meta:
        model = Image
        fields = ["id", "image", "product_variant"]


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, description, featured fields
    """

    class Meta:
        model = Category
        fields = [
            "id",
            "slug",
            "name",
            "icon",
        ]


class CreateProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant serializer for write only
    Return all fields
    """

    class Meta:
        model = ProductVariant
        fields = [
            "product",
            "price",
            "discount",
            "thumbnail",
            "stock",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant serializer for read only
    Return all fields
    """

    images = ImageSerializer(many=True, read_only=True)
    attribute_values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "price",
            "discount",
            "discount_price",
            "stock",
            "thumbnail",
            "attribute_values",
            "images",
        ]


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Product serializer for write only
    Return all fields
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "brand",
            "unit",
            "featured",
        ]

    def validate(self, data):
        if Product.objects.filter(
            name=data["name"], shop=self.context["request"].user.shop
        ).exists():
            raise serializers.ValidationError(
                {"name": "Product with this name already exists"}
            )


class BrandReadSerializer(serializers.ModelSerializer):
    """
    Brand return only id, slug, name
    """

    class Meta:
        model = Brand
        fields = ["id", "slug", "name"]


class SingleProductSerializer(serializers.ModelSerializer):
    """
    Single Product serializer for read only
    """

    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = AttributeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    shop = ShopProductSerializer(read_only=True)
    brand = BrandReadSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "shop",
            "description",
            "category",
            "rating",
            "brand",
            "unit",
            "featured",
            "variants",
            "reviews",
            "attributes",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer
    """

    shop = ShopProductSerializer(read_only=True)
    category: Field = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    discount = serializers.IntegerField(read_only=True)
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "slug",
            "name",
            "shop",
            "category",
            "rating",
            "price",
            "discount_price",
            "discount",
            "thumbnail",
        ]


class SingleCategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, description, featured fields
    """

    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "image",
            "slug",
            "parent",
            "description",
            "featured",
            "attributes",
        ]
