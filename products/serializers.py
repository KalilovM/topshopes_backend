from rest_framework import serializers
from rest_framework.serializers import Field

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
            "name",
            "icon",
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
        fields = ["attribute", "value"]

    def validate(self, data):
        if ProductAttributeValue.objects.filter(
            attribute=data["attribute"], product_variant=self.context["product_variant"]
        ).exists():
            raise serializers.ValidationError(
                {"detail": "Product attribute value already exists"}
            )
        return data

    def create(self, validated_data):
        product_variant = ProductVariant.objects.get(
            id=self.context["product_variant"].id
        )
        if product_variant.product.shop.user != self.context["user"]:
            raise serializers.ValidationError(
                {"detail": "You are not allowed to create product attribute value"}
            )
        validated_data["product_variant"] = product_variant
        product_attribute_value = ProductAttributeValue.objects.create(**validated_data)
        return product_attribute_value


class CreateProductAttributeSerializer(serializers.ModelSerializer):
    """
    Product variant attribute serializer for write only
    Return all fields
    """

    class Meta:
        model = ProductAttribute
        fields = ["name", "category"]

    def validate(self, data):
        if ProductAttribute.objects.filter(
            name=data["name"], category=data["category"]
        ).exists():
            raise serializers.ValidationError(
                {"detail": "Product attribute already exists"}
            )
        return data

    def create(self, validated_data):
        product = Product.objects.get(id=self.context["product"].id)
        if product.category != validated_data["category"]:
            raise serializers.ValidationError(
                {"detail": "Product category and attribute category must match"}
            )
        if product.shop.user != self.context["request"].user:
            raise serializers.ValidationError(
                {"detail": "You are not allowed to create product attribute"}
            )
        product_attribute = ProductAttribute.objects.create(**validated_data)
        return product_attribute


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


class SingleProductSerializer(serializers.ModelSerializer):
    """
    Single Product serializer for read only
    """

    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    shop = ShopProductSerializer(read_only=True)

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
    thumbnail = serializers.ImageField(read_only=True, source="thumbnail.url")

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
            "thumbnail",
        ]


class SingleCategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, description, featured fields
    """

    attributes = ProductAttributeSerializer(many=True, read_only=True)

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
