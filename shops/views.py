from rest_framework import mixins, permissions, viewsets
from .models import (
    Link,
    Shop,
)
from .serializers import (
    LinkSerializer,
    ShopSerializer,
    SingleShopSerializer,
)


class MyShopViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to edit user's shop
    available all methods
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SingleShopSerializer

    def perform_create(self, serializer):
        """
        On create set user to current user
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Returns only user's shop
        """
        return Shop.objects.filter(user=self.request.user.pk)


class ShopViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Viewset to get all Shops
    Only to get
    """

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]


class LinkViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for only user's shop links and can edit
    """

    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        On create save shop
        """
        serializer.save(shop=self.request.user.shop)

    def get_queryset(self):
        return Link.objects.filter(shop=self.request.user.shop)
