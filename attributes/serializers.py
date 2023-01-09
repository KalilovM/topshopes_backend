from rest_framework import serializers

from products.models import Product, ProductVariant

from .models import Attribute, AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    """
    Product attribute value serializer for read only
    Return only name and product
    """

    class Meta:
        model = AttributeValue
        fields = ["id", "product_variant", "attribute", "value"]


class CreateAttributeValueSerializer(serializers.ModelSerializer):
    """
    Product variant attribute value serializer for write only
    Return only name and product
    """

    class Meta:
        model = AttributeValue
        fields = ["attribute", "value"]

    def validate(self, data):
        if AttributeValue.objects.filter(
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
        product_attribute_value = AttributeValue.objects.create(**validated_data)
        return product_attribute_value


class CreateAttributeSerializer(serializers.ModelSerializer):
    """
    Product variant attribute serializer for write only
    Return all fields
    """

    class Meta:
        model = Attribute
        fields = ["name", "category"]

    def validate(self, data):
        if Attribute.objects.filter(
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
        product_attribute = Attribute.objects.create(**validated_data)
        return product_attribute


class AttributeSerializer(serializers.ModelSerializer):
    """
    Product variant attribute serializer for read only
    Return all fields
    """

    class Meta:
        model = Attribute
        fields = ["id", "name", "category"]
