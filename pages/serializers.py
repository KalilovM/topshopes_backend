from rest_framework import serializers
from .models import Page, PageNavigation, PageNavigationCategory


class PageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)

    class Meta:
        model = Page
        fields = "__all__"


class PageNavigationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    page = PageSerializer(required=True)

    class Meta:
        model = PageNavigation
        fields = "__all__"


class PageNavigationCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)
    page_navigation = PageNavigationSerializer(required=True)

    class Meta:
        model = PageNavigationCategory
        fields = "__all__"
