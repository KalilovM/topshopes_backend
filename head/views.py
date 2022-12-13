from rest_framework import permissions, viewsets
from shops.models import Brand, BrandType, Category, Product, Shop
from shops.serializers import (
    BrandSerializer,
    BrandTypeSerializer,
    CategorySerializer,
    ProductSerializer,
    ShopSerializer,
)

from users.models import Customer
from users.serializers import CustomerSerializer


class AdminUsersViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage users
    Allowed: All methods
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminShopViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage shops
    Allowed: All methods
    """

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage categories
    Allowed: All methods
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class AdminBrandViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage brands
    Allowed: All methods
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminBrandTypeViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage brand types
    Allowed: All methods
    """

    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminProductViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage products
    Allowed: All methods
    """

    queryset = Product.objects.all().prefetch_related("images")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


# class StaticPageViewSet(viewsets.ModelViewSet):
