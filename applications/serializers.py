from rest_framework import serializers
from .models import Application
import os

class CreateApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to create application
    """
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

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
