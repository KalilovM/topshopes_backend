from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Subquery, OuterRef
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework import mixins, permissions, viewsets

from attributes.models import Attribute
from attributes.serializers import AttributeSerializer
from head.serializers import AdminCustomerSerializer, AdminProductSerializer
from pages.models import Page, PageCategory, SiteSettings
from pages.serializers import (
    PageCategorySerializer,
    PageSerializer,
    CreatePageSerializer,
    SiteSettingsSerializer,
)
from posts.models import Post
from posts.serializers import PostSerializer
from products.models import Brand, BrandType, Category, Product, ProductVariant
from products.serializers import (
    BrandSerializer,
    BrandTypeSerializer,
    CreateCategorySerializer,
    CategorySerializer,
    CreateProductVariantSerializer,
    ProductVariantSerializer,
)
from products.serializers import SingleCategorySerializer
from shops.models import Shop
from shops.serializers import ShopSerializer, SingleShopSerializer
from sliders.models import Slide, Slider
from sliders.serializers import SliderSerializer, SlideSerializer
from users.models import Customer


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
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name"]


class AdminShopViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to manage shops
    Allowed: All methods
    """

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleShopSerializer
        return ShopSerializer


class AdminCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage categories
    Allowed: All methods
    """

    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["featured"]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleCategorySerializer
        if self.action in ["update", "create", "partial_update"]:
            return CreateCategorySerializer
        return CategorySerializer


class AdminBrandViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage brands
    Allowed: All methods
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["featured"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class AdminBrandTypeViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage brand types
    Allowed: All methods
    """

    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]


class AdminProductViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to manage products
    Allowed: All methods without create
    """

    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "rating", "created_at"]

    def get_queryset(self):
        """
        Returns only current user's shop products
        """
        return (
            Product.objects.prefetch_related("variants")
            .filter(shop=self.request.user.shop)  # type: ignore
            .annotate(
                overall_price=Subquery(
                    ProductVariant.objects.filter(product=OuterRef("pk")).values(
                        "overall_price"
                    )[:1]
                ),
                discount_price=Subquery(
                    ProductVariant.objects.filter(product=OuterRef("pk")).values(
                        "discount_price"
                    )[:1]
                ),
                discount=Subquery(
                    ProductVariant.objects.filter(product=OuterRef("pk")).values(
                        "discount"
                    )[:1]
                ),
                thumbnail=Subquery(
                    ProductVariant.objects.filter(product=OuterRef("pk")).values(
                        "thumbnail"
                    )[:1]
                ),
            )
        )

    def get_serializer_class(self):
        return AdminProductSerializer

    def update(self, request, *args, **kwargs):
        """
        Update product
        """
        if request.data["category"]:
            product = self.get_object()
            variants = product.variants.all()
            for variant in variants:
                variant.attribute_values.all().delete()
        return super().update(request, *args, **kwargs)


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
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePageSerializer
        return PageSerializer


class AdminPageCategoryViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage page categories
    Allowed: All methods
    """

    queryset = PageCategory.objects.all()
    serializer_class = PageCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]


@extend_schema(
    description="Get all sliders with their slides",
    responses={200: SliderSerializer(many=True)},
)
class AdminSliderViewSet(viewsets.ModelViewSet):
    """
    Viewset to manage sliders
    Allowed: All methods
    """

    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"


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

    def get_object(self):
        return SiteSettings.objects.first()


class AdminProductVariantViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to manage product variants
    Allowed: All methods
    """

    queryset = ProductVariant.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return CreateProductVariantSerializer
        return ProductVariantSerializer


class AdminAttributesViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
