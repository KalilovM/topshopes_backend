from rest_framework import mixins, permissions, viewsets
from drf_spectacular.utils import extend_schema

from .models import Slider
from .serializers import (
    SliderSerializer,
    CreateSliderSerializer,
    SingleSliderSerializer,
)


@extend_schema(
    description="SliderViewSet to read_only",
    responses={200: SliderSerializer},
    tags=["All"],
)
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
        elif self.action == "retrieve":
            return SingleSliderSerializer
        return SliderSerializer
