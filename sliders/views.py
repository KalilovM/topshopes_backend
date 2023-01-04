from rest_framework import mixins, permissions, viewsets

from .models import Slider
from .serializers import SliderSerializer


class SliderViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SliderViewSet to read_only
    """

    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
