from rest_framework import serializers
from rest_framework.serializers import Field
from .models import Review


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("rating", "comment", "product_variant")

    def create(self, validated_data):
        user = self.context["request"].user
        shop = self.context["product"].shop
        product = self.context["product"]
        review = Review.objects.create(user=user,product=product, shop=shop, **validated_data)
        return review


class ReviewSerializer(serializers.ModelSerializer):
    user: Field = serializers.SlugRelatedField(
        read_only=True,
        slug_field="first_name",
    )
    product_variant: Field = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Review
        fields = "__all__"
