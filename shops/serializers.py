from rest_framework import serializers
from core.helpers import ImageUrlField
from core.mixins import CommonRelatedField
from shops.mixins import CustomRelatedField

from users.serializers import CustomerSerializer
from .models import (
    Link,
    Shop,
    Size,
    Color,
    BrandType,
    Image,
    Category,
    Brand,
    Product,
    Review,
)


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for Link model
    Return name and link
    """

    class Meta:
        model = Link
        fields = ["name", "link"]


class SizeSerializer(serializers.ModelSerializer):
    """
    Size serialzier
    Return all fields
    """

    id = serializers.ReadOnlyField()

    class Meta:
        model = Size
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    """
    Color serializer
    Return all fields
    """

    id = serializers.ReadOnlyField()

    class Meta:
        model = Color
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand serializer able to select fields to represent
    Return all fields
    """

    id = serializers.ReadOnlyField()

    class Meta:
        model = Brand
        fields = "__all__"


class BrandTypeSerializer(serializers.ModelSerializer):
    """
    Serialzier for brand type
    Return all fields
    """

    id = serializers.ReadOnlyField()

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
        fields = ["id", "image"]


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, descirption, featured fields
    """

    id = serializers.ReadOnlyField()

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


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serialzier
    Return necessary fields for list view
    """

    id = serializers.ReadOnlyField()
    sizes = CustomRelatedField(many=True, queryset=Size.objects.all())
    color = CustomRelatedField(many=True, queryset=Color.objects.all())
    shop = CommonRelatedField(model=Shop, serializer=ShopSerializer, read_only=True)
    categories = CustomRelatedField(many=True, queryset=Category.objects.all())
    images = ImageUrlField(many=True, read_only=True)
    brand = ImageUrlField(many=False, read_only=True)
    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "shop",
            "title",
            "brand",
            "price",
            "size",
            "colors",
            "discount",
            "thumbnail",
            "images",
            "categories",
            "status",
            "rating",
            "unit",
            "published",
        ]


class SingleShopSerializer(serializers.ModelSerializer):
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


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review serializer
    Return all fields
    """

    id = serializers.ReadOnlyField()
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
