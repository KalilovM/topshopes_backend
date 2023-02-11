from rest_framework import viewsets, mixins, permissions
from drf_spectacular.utils import extend_schema
from .serializers import (
    CreatePaymentSerialzier,
    PaymentSerializer,
    SinglePaymentSerializer,

)
from .models import Payment, TransferMoney


@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    request=CreatePaymentSerialzier,
    tags=["Owner"],
)
class UserPaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    List payments
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        super().get_serializer_class()
        return PaymentSerializer


@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    request=CreatePaymentSerialzier,
    tags=["admin"],
)
class AdminPaymentViewSet(viewsets.ModelViewSet):
    """Admin payment viewset"""

    permission_classses = [permissions.IsAdminUser]
    queryset = Payment.objects.all()

    def update(self, request, *args, **kwargs):
        if request.data.get("is_verified"):
            payment = self.get_object()
            payment.orders.update(status="paid")
        else:
            payment = self.get_object()
            payment.orders.update(status="payment_error")
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        return PaymentSerializer

class AdminMoneyTransferViewSet(viewsets.ModelViewSet):
    """Admin money transfer viewset"""

    permission_classses = [permissions.IsAdminUser]
    queryset = TransferMoney.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        return PaymentSerializer
