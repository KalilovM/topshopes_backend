from rest_framework import serializers
from rest_framework.serializers import Field

from products.models import (
    Brand,
    BrandType,
    Category,
    Color,
    Image,
    Product,
    ProductVariant,
    Review,
    Size,
)
from users.serializers import CustomerSerializer


class SizeSerializer(serializers.ModelSerializer):
    """
    Size serializer
    Return all fields
    """

    class Meta:
        model = Size
        fields = ["id", "name"]


class ColorSerializer(serializers.ModelSerializer):
    """
    Color serializer
    Return all fields
    """

    class Meta:
        model = Color
        fields = ["id", "name", "color"]


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


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review serializer
    Return all fields
    """

    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer to Product variant read_only
    """

    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "color",
            "size",
            "thumbnail",
            "status",
            "stock",
            "price",
            "discount",
            "discount_price",
        ]


class CreateProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer to Product variant write_only
    """

    size: Field = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Size.objects.all()
    )
    color: Field = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Color.objects.all()
    )

    class Meta:
        model = ProductVariant
        fields = "__all__"

    def validate_discount(self, value):
        if 0 <= value <= 100:
            return value

        return serializers.ValidationError(
            "discount should be more or equal 0 and less or equal 100"
        )


class ProductSerializer(serializers.ModelSerializer):
    from shops.serializers import ShopSerializer

    """
    Product serializer to read_only
    Return necessary fields for list view
    """

    shop = ShopSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "shop",
            "title",
            "brand",
            "category",
            "rating",
            "unit",
            "published",
            "variants",
            "reviews",
        ]


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Product serializer to write_only
    Return necessary fields for list view
    """

    class Meta:
        model = Product
        fields = [
            "title",
            "rating",
            "unit",
            "published",
        ]
