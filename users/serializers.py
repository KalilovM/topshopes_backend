from rest_framework import serializers
from rest_framework.serializers import Field

from .models import Address, Customer
from roles.serializers import RoleSerializer


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

    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
        ]


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
