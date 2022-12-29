from rest_framework import mixins, viewsets, permissions
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from core.permissions import IsOwner, HasShop


from products.models import (
    Size,
    Color,
    BrandType,
    Image,
    Category,
    Brand,
    Product,
    Review,
    ProductVariant,
)

from products.serializers import (
    CreateProductSerializer,
    SizeSerializer,
    ColorSerializer,
    BrandSerializer,
    BrandTypeSerializer,
    ImageSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductVariantSerializer,
    CreateProductVariantSerializer,
    CreateReviewSerializer,
)


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Product viewset to get all products
    Only get method allowed
    """

    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer


@extend_schema(
    description="Viewset to create product",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    responses={201: ProductVariantSerializer},
    tags=["Products"],
)
class ProductVariantViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Product variant viewset to create product variants
    Only create method allowed
    """

    permission_classes = [permissions.IsAuthenticated, HasShop, IsOwner]

    def get_queryset(self):
        """
        Returns only current user's shop products
        """
        return ProductVariant.objects.filter(
            product__shop=self.request.user.shop  # type: ignore
        )

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return CreateProductVariantSerializer
        return ProductVariantSerializer


@extend_schema(
    description="Viewset to edit user's shop",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    responses={200: ProductSerializer},
    tags=["Shops"],
)
class ShopProductViewSet(viewsets.ModelViewSet):
    """
    Viewset allows the owner of shop to edit products
    """

    # Add new permission is owner
    permission_classes = [permissions.IsAuthenticated, IsOwner, HasShop]

    def get_queryset(self):
        """
        Returns only current user's shop products
        """
        return Product.objects.prefetch_related("variants").filter(
            shop=self.request.user.shop  # type: ignore
        )

    def perform_create(self, serializer):
        """
        On create product set shop to user's
        """
        if self.request.user.shop is not None:
            serializer.save(shop=self.request.user.shop)  # type: ignore

        raise serializers.ValidationError("Shop not found")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        return ProductSerializer


class SizeViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Size viewset every user can create own sizes for product
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop]


class ColorViewSet(viewsets.ModelViewSet):
    """
    Color viewset every user can create own color for product
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop]


class BrandTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list
    """

    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to get, destroy and update product images
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list Categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list Brands
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ReviewViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset to get current product reviews
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Returns only current product reviews
        """
        return Review.objects.filter(product=self.kwargs["product_pk"])

    def perform_create(self, serializer):
        """
        On create review set user to current user
        """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateReviewSerializer
        return ReviewSerializer
