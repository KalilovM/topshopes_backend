from rest_framework import serializers
from .models import Slider, Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):
    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = ["title", "slug", "slides"]


class CreateSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["title"]
