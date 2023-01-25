from rest_framework import viewsets, mixins, permissions
from drf_spectacular.utils import extend_schema
from core.permissions import HasShop
from .serializers import CreatePaymentSerialzier, PaymentSerializer, SinglePaymentSerializer
from .models import Payment


@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    request=CreatePaymentSerialzier,
    tags=["Owner"])
class UserPaymentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    List payments
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def get_seiralizer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        return PaymentSerializer
    

@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    tags=["Owner"]
)
class ShopPaymentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List payments
    """
    permission_classes = [permissions.IsAuthenticated, HasShop]
    
    def get_queryset(self):
        return Payment.objects.filter(shop=self.request.shop)
    
    def get_seiralizer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        return PaymentSerializer
    

@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    request=CreatePaymentSerialzier,
    tags=["Admin"]
)
class AdminPaymentViewSet(viewsets.ModelViewSet):
    """Admin payment viewset"""
    
    permission_classses = [permissions.IsAdminUser]
    queryset = Payment.objects.all()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        return PaymentSerializer