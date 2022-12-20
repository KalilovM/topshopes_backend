from rest_framework import serializers
from .models import Page, PageCategory


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class PageCategorySerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)

    class Meta:
        model = PageCategory
        fields = "__all__"
