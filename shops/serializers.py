from rest_framework import serializers
from core.helpers import ImageUrlField
from core.mixins import CommonRelatedField
from shops.mixins import CategoryRelatedField

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


# Not important serializers
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["name", "link"]


class SizeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Size
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Color
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super().__init__(self, *args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field in existing - allowed:
                self.fields.pop(field)

    class Meta:
        model = Brand
        fields = "__all__"


class BrandTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = BrandType
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image"]


class CategorySerializer(serializers.ModelSerializer):
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
    id = serializers.ReadOnlyField()
    user = CustomerSerializer()

    class Meta:
        model = Shop
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    size = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    colors = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    shop = CommonRelatedField(model=Shop, serializer=ShopSerializer, read_only=True)
    categories = CategoryRelatedField(many=True)
    # how to set only image to field brand (brand image only, now it's object and image)
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
    id = serializers.ReadOnlyField()
    user = CustomerSerializer(read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
