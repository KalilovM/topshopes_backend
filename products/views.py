from rest_framework import mixins, viewsets, permissions
from .services import buy_product
from orders.serializers import CreateOrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from core.permissions import IsOwner, HasShop

from reviews.models import Review
from reviews.serializers import CreateReviewSerializer, ReviewSerializer


from products.models import (
    BrandType,
    Image,
    Category,
    Brand,
    Product,
    ProductVariant,
)

from products.serializers import (
    CreateProductSerializer,
    BrandSerializer,
    BrandTypeSerializer,
    ImageSerializer,
    CategorySerializer,
    ProductSerializer,
    CreateProductAttributeSerializer,
    ProductVariantSerializer,
    CreateProductVariantSerializer,
    CreateProductAttributeValueSerializer,
    ProductAttributeValueSerializer,
)


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Product viewset to get all products
    Only get method allowed
    """

    queryset = Product.objects.all().prefetch_related("variants")
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    @action(detail=True, methods=["post"])
    @extend_schema(
        description="Create attribute for product",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        responses={201: CreateProductAttributeSerializer},
        tags=["Products"],
    )
    def create_attribute(self, request, pk=None):
        """
        Create product attribute
        """
        product = self.get_object()
        serializer = CreateProductAttributeSerializer(
            data=request.data, context={"product": product}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    @extend_schema(
        description="Create review for product",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        responses={201: CreateReviewSerializer},
        tags=["Reviews"],
    )
    def review(self, request, pk=None):
        """
        Review product
        """
        product = self.get_object()
        serializer = CreateReviewSerializer(
            data=request.data, context={"product": product}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    @action(detail=True, methods=["post"])
    @extend_schema(
        description="Create product variant attribute",
        responses={201: CreateProductAttributeSerializer},
        tags=["Product Attributes"],
    )
    def create_attribute_value(self, request, pk=None):
        """
        Create product variant attribute
        """
        product_variant = self.get_object()
        serializer = CreateProductAttributeValueSerializer(
            data=request.data, context={"product_variant": product_variant}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    @extend_schema(
        description="Buy product variant",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        responses={201: CreateOrderSerializer},
        tags=["Orders"],
    )
    def buy(self, request, pk=None):
        """
        Buy product variant
        """
        product_variant = self.get_object()
        data = buy_product(
            product_variant=product_variant,
            quantity=request.data["quantity"],
            user=request.user,
            address=request.data["address"],
            shop=product_variant.product.shop,
        )
        return Response(data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Returns only current user's shop products
        """
        return ProductVariant.objects.filter(
            product__shop=self.request.user.shop  # type: ignore
        ).prefetch_related("attributes", "images")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
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
        else:
            raise serializers.ValidationError("Shop not found")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        return ProductSerializer


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
