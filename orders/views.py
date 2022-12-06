from .serializers import OrderItemSerializer, OrderSerializer
from .models import Order, OrderItem
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    """
    Viewset with [LIST, RETRIEVE, CREATE] methods
    """

    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        return (
            Order.objects.prefetch_related("items")
            .all()
            .filter(user=self.request.user.pk)
        )


class OrderItemViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    View to create Item fro Order
    """

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class ShopOrderViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            Order.objects.prefetch_related("items")
            .all()
            .filter(shop=self.request.user.shop)
        )
