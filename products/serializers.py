from rest_framework import serializers

from products.models import (
    Brand,
    BrandType,
    Category,
    Image,
    Product,
    ProductVariant,
    ProductAttribute,
    ProductAttributeValue,
)
from shops.models import Shop
from reviews.serializers import ReviewSerializer


class ShopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name"]


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
            "name",
            "icon",
            "image",
            "slug",
            "parent",
            "description",
            "featured",
        ]


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    Product attribute value serializer for read only
    Return only name and product
    """

    class Meta:
        model = ProductAttributeValue
        fields = ["id", "product_variant", "attribute", "value"]


class CreateProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    Product variant attribute value serializer for write only
    Return only name and product
    """

    class Meta:
        model = ProductAttributeValue
        fields = ["product_variant", "attribute", "value"]


class CreateProductAttributeSerializer(serializers.ModelSerializer):
    """
    Product variant attribute serializer for write only
    Return all fields
    """

    class Meta:
        model = ProductAttribute
        fields = ["name", "category"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    Product variant attribute serializer for read only
    Return all fields
    """

    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "category"]


class CreateProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant serializer for write only
    Return all fields
    """

    class Meta:
        model = ProductVariant
        fields = [
            "name",
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
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "name",
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
        fields = ["name", "description", "category", "brand", "unit", "featured"]

    def validate(self, data):
        if Product.objects.filter(
            name=data["name"], shop=self.context["request"].user.shop
        ).exists():
            raise serializers.ValidationError(
                {"name": "Product with this name already exists"}
            )


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer for read only
    """

    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
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
