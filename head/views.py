from rest_framework import permissions, viewsets
from rest_framework import mixins
from shops.models import Shop
from products.models import Product, Brand, Category, BrandType, ProductVariant
from shops.serializers import (
    ShopSerializer,
)
from products.serializers import (
    BrandSerializer,
    BrandTypeSerializer,
    CategorySerializer,
    ProductVariantSerializer,
    CreateProductVariantSerializer,
)

from head.serializers import AdminProductSerializer, AdminCustomerSerializer, AdminCreateProductSerializer

from users.models import Customer
from users.serializers import CustomerSerializer

from posts.models import Post
from posts.serializers import PostSerializer

from pages.models import Page, PageCategory, SiteSettings
from pages.serializers import (
    PageSerializer,
    PageCategorySerializer,
    SiteSettingsSerializer,
)

from sliders.models import Slider, Slide
from sliders.serializers import (
    SliderSerializer,
    SlideSerializer,
)


class AdminUsersViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to manage users
    Allowed: All methods without create
    """

    queryset = Customer.objects.all()
    serializer_class = AdminCustomerSerializer
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

    queryset = Product.objects.all().prefetch_related("variants")
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return AdminCreateProductSerializer
        return AdminProductSerializer


class AdminPostViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage posts
    Allowed: All methods
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdminPageViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage pages
    Allowed: All methods
    """

    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminPageCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage page categories
    Allowed: All methods
    """

    queryset = PageCategory.objects.all()
    serializer_class = PageCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class AdminSliderViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage sliders
    Allowed: All methods
    """

    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminSlideViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage slides
    Allowed: All methods
    """

    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminSiteSettingsViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Viewset to manage site settings
    Allowed: GET, PUT, PATCH
    """

    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminProductVariantViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage product variants
    Allowed: All methods
    """

    queryset = ProductVariant.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductVariantSerializer
        return ProductVariantSerializer
