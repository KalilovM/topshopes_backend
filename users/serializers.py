from rest_framework import serializers
from .models import Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
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


from .mixins import CustomerRelatedField
class AddressSerializer(serializers.ModelSerializer):
    user = CustomerRelatedField()
    class Meta:
        model = Address
        fields = "__all__"
