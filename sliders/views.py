from rest_framework import mixins, permissions, viewsets

from .models import Slider
from .serializers import SliderSerializer, CreateSliderSerializer


class SliderViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SliderViewSet to read_only
    """

    queryset = Slider.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "create":
            return CreateSliderSerializer
        return SliderSerializer
