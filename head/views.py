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

from posts.models import Post
from posts.serializers import PostSerializer

from pages.models import Page, PageNavigation, PageNavigationCategory
from pages.serializers import (
    PageSerializer,
    PageNavigationSerializer,
    PageNavigationCategorySerializer,
)


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


class AdminPostViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage posts
    Allowed: All methods
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminPageViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage pages
    Allowed: All methods
    """

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminPageNavigationViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage page navigations
    Allowed: All methods
    """

    queryset = PageNavigation.objects.all()
    serializer_class = PageNavigationSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminPageNavigationCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage page navigation categories
    Allowed: All methods
    """

    queryset = PageNavigationCategory.objects.all()
    serializer_class = PageNavigationCategorySerializer
    permission_classes = [permissions.IsAdminUser]
