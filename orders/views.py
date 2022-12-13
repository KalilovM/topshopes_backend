from rest_framework.serializers import Serializer
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
    Viewset for user orders
    Allow to get and create only
    """

    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        """
        On get method return only current user's orders
        """
        return (
            Order.objects.prefetch_related("items")
            .all()
            .filter(user=self.request.user.pk)
        )

    def perform_create(self, serializer: Serializer):
        """
        On create set current user as order's user
        """
        serializer.save(user=self.request.user.pk)


class OrderItemViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    View to create Item for Order
    Only create
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
    """
    Viewset for Shop's orders
    Can update and get only
    """

    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        Only current user's shop orders
        """
        return (
            Order.objects.prefetch_related("items")
            .all()
            .filter(shop=self.request.user.shop)
        )
