from django.contrib.auth.hashers import make_password
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.permissions import IsAnonymous
from .models import Address, Customer
from rest_framework import permissions
from .serializers import AddressSerializer, CustomerSerializer


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAnonymous]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        return Customer.objects.all().filter(id=self.request.user.id)

    def get_object(self, pk=None):
        return self.request.user

    def perform_create(self, serializer):
        print(self.request.data)
        serializer.save(password=make_password(self.request.data["password"]))


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return Address.objects.all().filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
