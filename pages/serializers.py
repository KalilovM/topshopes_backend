from rest_framework import serializers
from .models import Page, PageCategory, SiteSettings


class PageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PageCategory
        fields = "__all__"

class PageCategorySerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)
    class Meta:
        model = PageCategory
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    category = PageCategorySerializer(read_only=True)


class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"



class CreatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"
