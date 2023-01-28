from rest_framework import serializers
from orders.serializers import OrderSerializer, OrderInfoSerializer
from .models import Payment, TransferMoney
from head.serializers import AdminShopSerializer


class CreatePaymentSerialzier(serializers.ModelSerializer):
    """
    Payment serialzier to create only
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "confirm_photo",
            "phone_number",
            "bank_account",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment serialzier to read only
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "phone_number",
            "bank_account",
            "is_verified",
        ]


class SinglePaymentSerializer(serializers.ModelSerializer):
    """
    Payment serialzier to read only
    """

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "confirm_photo",
            "phone_number",
            "bank_account",
            "is_verified",
            "orders",
        ]


class CreateTransferMoneySerializer(serializers.ModelSerializer):
    """
    TransferMoney serialzier to create only
    """

    class Meta:
        model = TransferMoney
        fields = ["id", "order", "amount", "shop", "tax"]


class TransferMoneySerializer(serializers.ModelSerializer):
    """
    TransferMoney serialzier to read only
    """
    shop = AdminShopSerializer(read_only=True)
    order = OrderInfoSerializer(read_only=True)

    class Meta:
        model = TransferMoney
        fields = ["id", "order", "amount", "shop", "tax", "confirm_photo"]
