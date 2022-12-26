from django.db.transaction import atomic
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer


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

    def get_serializer_class(self):
        return OrderSerializer(context={"request": self.request})


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
