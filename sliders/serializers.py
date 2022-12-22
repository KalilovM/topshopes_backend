from rest_framework import serializers
from .models import Slider, Slide


class SlideSerializer(serializers.Serializer):
    class Meta:
        model = Slide
        fields = "__all__"


class SliderSerializer(serializers.Serializer):
    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Slider
        fields = "__all__"
