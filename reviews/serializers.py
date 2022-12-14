from rest_framework import serializers
from users.models import Customer
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
        review = Review.objects.create(
            user=user, product=product, shop=shop, **validated_data
        )
        return review


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "avatar")


class ReviewSerializer(serializers.ModelSerializer):
    product_variant: Field = serializers.StringRelatedField()
    user = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
