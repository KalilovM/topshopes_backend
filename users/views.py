from django.contrib.auth.hashers import make_password
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.permissions import IsAnonymous

from .models import Address, Customer
from .serializers import (AddressSerializer, CreateAddressSerializer,
                          CreateCustomerSerializer, CustomerSerializer)


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    Viewset to create,update and retrieve current user
    """

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CustomerSerializer
        return CreateCustomerSerializer

    def get_permissions(self):
        """
        Create available only for anonymous users
        """
        if self.action == "create":
            self.permission_classes = [IsAnonymous]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """
        If user is authenticated return only current user
        """
        return Customer.objects.all().filter(id=self.request.user.id)

    def get_object(self, pk=None):
        return self.request.user

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data["password"]))


class AddressViewSet(ModelViewSet):
    """
    Address Viewset allowed all methods
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return Address.objects.all().filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CreateAddressSerializer
        return AddressSerializer
