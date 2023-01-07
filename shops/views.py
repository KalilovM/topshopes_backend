from rest_framework import mixins, permissions, viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.permissions import HasShop, IsOwner

from .models import Link, Shop
from .serializers import (
    CreateShopSerializer,
    LinkSerializer,
    ShopSerializer,
    SingleShopSerializer,
)


@extend_schema(
    description="Viewset to edit user's shop",
    request=CreateShopSerializer,
    responses={200: SingleShopSerializer},
    tags=["Owner"],
)
class MyShopViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to edit user's shop
    available all methods
    """

    queryset = Shop.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateShopSerializer
        return SingleShopSerializer

    def perform_create(self, serializer):
        """
        On create set user to current user
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Set permissions
        """
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), HasShop()]

    def get_object(self):
        """
        Return only user's shop
        """
        return self.request.user.shop


@extend_schema(
    description="Viewset to get all Shops",
    parameters=[OpenApiParameter("slug", OpenApiTypes.STR, OpenApiParameter.PATH)],
    responses={200: ShopSerializer},
    tags=["All"],
)
class ShopViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Viewset to get all Shops
    Only to get
    """

    queryset = Shop.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleShopSerializer
        return ShopSerializer


@extend_schema(
    description="Viewset to control only user's shop links",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    responses={200: LinkSerializer},
    tags=["Owner"],
)
class LinkViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to control only user's shop links
    Maximum 5 links per shop
    """

    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop, IsOwner]

    def perform_create(self, serializer):
        """
        On create save shop
        """
        serializer.save(shop=self.request.user.shop)

    def get_queryset(self):
        """
        Return only user's shop links
        """
        return Link.objects.filter(shop=self.request.user.shop)
