from rest_framework import mixins, permissions, viewsets

from core.permissions import HasShop

from .models import AttributeValue, Attribute
from .serializers import AttributeValueSerializer, AttributeSerializer


class AttributeValueViewset(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Viewset to delete and update product attributes
    Awailable only for sellers
    """

    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop]
