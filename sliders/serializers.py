from rest_framework import serializers
from .models import Slider, Slide
from rest_framework.serializers import Field


class SlideSerializer(serializers.ModelSerializer):
    slider: Field = serializers.SlugRelatedField(
        slug_field="slug", queryset=Slider.objects.all()
    )

    class Meta:
        model = Slide
        fields = "__all__"


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["title", "slug"]


class SingleSliderSerializer(serializers.ModelSerializer):

    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = ["title", "slug", "slides"]


class CreateSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["title"]
