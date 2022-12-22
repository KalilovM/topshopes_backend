from rest_framework import serializers
from core.mixins import CommonRelatedField
from shops.mixins import CustomRelatedField, CustomRelatedFieldWithImage
from shops.models import Shop
from products.models import Product, Size, Color, Brand, Category
from shops.serializers import ShopSerializer
from products.serializers import ImageSerializer


class AdminProductSerializer(serializers.ModelSerializer):
    """
    Product serialzier
    Return necessary fields for list view
    """

    id = serializers.ReadOnlyField()
    sizes = CustomRelatedField(many=True, queryset=Size.objects.all())
    colors = CustomRelatedField(many=True, queryset=Color.objects.all())
    shop = CommonRelatedField(model=Shop, serializer=ShopSerializer, read_only=True)
    categories = CustomRelatedField(many=True, queryset=Category.objects.all())
    images = ImageSerializer(many=True, read_only=True)
    brand = CustomRelatedFieldWithImage(many=False, queryset=Brand.objects.all())

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
            "sizes",
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
