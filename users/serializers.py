from rest_framework import serializers

from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer to customer
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "password",
            "dateOfBirth",
            "verified",
        ]


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for addresses
    """

    class Meta:
        model = Address
        fields = "__all__"
