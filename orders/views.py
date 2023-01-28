from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from core.permissions import HasShop, IsOwner
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer


@extend_schema(
    description="Create order",
    parameters=[
        OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH),
    ],
    request=CreateOrderSerializer,
    responses={201: OrderSerializer},
    tags=["Orders"],
)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
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
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return OrderSerializer


@extend_schema(
    description="Viewset for Shop's orders",
    parameters=[
        OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH),
    ],
    responses={200: OrderSerializer},
    tags=["Orders"],
)
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

    permission_classes = (permissions.IsAuthenticated, HasShop, IsOwner)

    def get_queryset(self):
        """
        Only current user's shop orders
        """
        return (
            Order.objects.all()
            .filter(shop=self.request.user.shop)
            .exclude(status__in=["payment_error", "pending"])
        )

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOrderSerializer(context={"request": self.request})
        return OrderSerializer
