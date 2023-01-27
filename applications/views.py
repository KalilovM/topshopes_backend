from rest_framework import viewsets, mixins, permissions
from .serializers import (
    CreateApplicationSerializer,
    ApplicationSerializer,
    SingleApplicationSerializer,
)
from .models import Application
from drf_spectacular.utils import extend_schema


@extend_schema(responses=ApplicationSerializer, tags=["Owner"])
class ApplicationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Application view set to read only
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleApplicationSerializer
        if self.action == "create":
            return CreateApplicationSerializer
        return ApplicationSerializer

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
