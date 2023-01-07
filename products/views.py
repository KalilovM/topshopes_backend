from rest_framework import mixins, viewsets, permissions
from .services import buy_product
from orders.serializers import CreateOrderSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from core.permissions import IsOwner, HasShop

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
    ProductAttributeSerializer,
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

    lookup_field = "slug"
    queryset = Product.objects.all().prefetch_related("variants")
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    @extend_schema(
        description="Create review for product",
        request=CreateReviewSerializer,
        responses={201: ReviewSerializer},
        tags=["Reviews"],
    )
    @action(detail=True, methods=["post"])
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
    description="Product variant viewset to create product variants",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=CreateProductVariantSerializer,
    responses={200: ProductVariantSerializer},
    tags=["My", "Variants"],
)
class ProductVariantViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Product variant viewset to create product variants
    Only create method allowed
    """

    permission_classes = [permissions.IsAuthenticated, HasShop]

    @extend_schema(
        description="Create product variant attribute",
        request=CreateProductAttributeValueSerializer,
        responses={201: ProductAttributeSerializer},
        tags=["Product Attributes"],
    )
    @action(detail=True, methods=["post"])
    def create_attribute_value(self, request, pk=None):
        """
        Create product variant attribute
        """
        product_variant = self.get_object()
        serializer = CreateProductAttributeValueSerializer(
            data=request.data,
            context={"product_variant": product_variant, "user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Buy product variant",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=CreateOrderSerializer,
        responses={201: OrderSerializer},
        tags=["Buy"],
    )
    @action(
        detail=True,
        methods=["post"],
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
        ).prefetch_related("attribute_values", "images")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CreateProductVariantSerializer
        return ProductVariantSerializer


@extend_schema(
    description="Viewset to edit user's shop",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=CreateProductSerializer,
    responses={200: ProductSerializer},
    tags=["My", "Products"],
)
class ShopProductViewSet(viewsets.ModelViewSet):
    """
    Viewset allows the owner of shop to edit products
    """

    lookup_field = "slug"
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

    @action(detail=True, methods=["post"])
    @extend_schema(
        description="Create attribute for product",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=CreateProductAttributeSerializer,
        responses={201: CreateProductAttributeSerializer},
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


@extend_schema(
    description="Brand Types for products",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=BrandTypeSerializer,
    responses={200: BrandTypeSerializer},
    tags=["Products additions"],
)
class BrandTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list
    """

    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    description="Images for products variants",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=ImageSerializer,
    responses={200: ImageSerializer},
    tags=["Products additions"],
)
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


@extend_schema(
    description="Categories for products",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=CategorySerializer,
    responses={200: CategorySerializer},
    tags=["Products additions"],
)
class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list Categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(
    description="Brands for products",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=BrandSerializer,
    responses={200: BrandSerializer},
    tags=["Products additions"],
)
class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list Brands
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
