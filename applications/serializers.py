import os

from shops.serializers import CreateShopSerializer
from rest_framework import serializers

from .models import Application


class CreateApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to create application
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)

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
            "user",
        ]

    def validate_document(self, value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = [".pdf"]
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension.")
        return value

    def validate_user(self, value):
        if Application.objects.filter(user=value, status="moderation").count() >= 1:
            raise serializers.ValidationError("Couldn't create more than 1 application")
        return value


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer to read only
    """

    class Meta:
        model = Application
        fields = ["id", "user", "document", "short_name", "status"]


    def validate_status(self,value):
        if value == "approved":
            self.instance.user.is_seller = True
            self.instance.user.save()
        return value


class SingleApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer single instance to read only
    """

    class Meta:
        model = Application
        fields = "__all__"
