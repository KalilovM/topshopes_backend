from rest_framework import serializers
from rest_framework.serializers import Field
import os

from roles.serializers import RoleSerializer

from .models import Address, Customer, Seller, Application


class CreateCustomerSerializer(serializers.ModelSerializer):
    """
    Serialzier to create customer
    """

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "password",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer Customer to read_only
    """


    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "is_superuser",
            "is_seller"
        ]


class CreateApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to create application
    """

    class Meta:
        model = Application
        fields = [
            "id",
            "document",
            "status",
            "INN",
            "short_name",
            "full_name",
            "registration_form",
            "address",
            "owner",
            "bank_account",
            "bik",
            "shop_name",
            "customer"
        ]

    def validate_document(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf']
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError('Unsupported file extension.')
        return value


class CreateAddressSerializer(serializers.ModelSerializer):
    """
    Serializer to create addresses
    """

    user: Field = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = ["user", "country", "city", "street", "phone"]


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer to read only addresses
    """

    class Meta:
        model = Address
        fields = ["id", "user", "country", "city", "street", "phone"]
