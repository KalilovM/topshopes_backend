from rest_framework import serializers
from orders.serializers import OrderSerializer
from .models import Payment


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
    orders = OrderSerializer(many=True,read_only=True)
    
    
    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "confirm_photo",
            "phone_number",
            "bank_account",
            "is_verified",
            "orders"
        ]
