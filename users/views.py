from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema
from core.permissions import IsAnonymous

from .models import Address, Customer
from .serializers import (
    AddressSerializer,
    CreateAddressSerializer,
    CreateCustomerSerializer,
    CustomerSerializer,
)

from applications.serializers import CreateApplicationSerializer


@extend_schema(
    description="CustomerViewSet to create,update and retrieve current user",
    responses={200: CustomerSerializer},
    tags=["Owner"],
)
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

    @extend_schema(
        description="Create application to become seller",
        responses={200: CreateApplicationSerializer},
        request=CreateApplicationSerializer,
        tags=["Owner"],
    )
    @action(detail=False, methods=['post'])
    def create_application(self, request, pk=None):
        serializer = CreateApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        try:
            email = EmailMessage(
                "Application to become seller",
                f"User {request.user.email} send application to become seller \n"
                f"INN {request.data['INN']} \n"
                f"Short name {request.data['short_name']} \n"
                f"Full name {request.data['full_name']} \n"
                f"Owner {request.data['owner']} \n"
                f"Bank account {request.data['bank_account']} \n"
                f"BIK {request.data['bik']} \n",
                settings.EMAIL_HOST_USER, ["kalilov_m@auca.kg"])
            email.attach(request.data['document'].name, request.data['document'].read(),
                         request.data['document'].content_type)
            email.send()
        except Exception as e:
            print(e)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    description="Address Viewset allowed all methods",
    request=CreateAddressSerializer,
    responses={200: AddressSerializer},
    tags=["Owner"],
)
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
