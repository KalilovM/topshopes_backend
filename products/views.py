from django.db.models import OuterRef, Subquery
from django.db.transaction import atomic
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import ProductFilter

from attributes.serializers import AttributeSerializer, CreateAttributeValueSerializer
from core.permissions import HasShop, IsOwner
from orders.serializers import CreateOrderSerializer, OrderSerializer
from products.models import Brand, BrandType, Category, Image, Product, ProductVariant
from products.serializers import (
    BrandSerializer,
    BrandTypeSerializer,
    CategorySerializer,
    CreateProductSerializer,
    CreateProductVariantSerializer,
    ImageSerializer,
    ProductSerializer,
    ProductVariantSerializer,
    SingleCategorySerializer,
    SingleProductSerializer,
)
from reviews.serializers import CreateReviewSerializer, ReviewSerializer


@extend_schema_view(
    list=extend_schema(
        description="Get list of products",
        responses={200: ProductSerializer},
        tags=["All"],
    ),
    retrieve=extend_schema(
        description="Get one product",
        responses={200: SingleProductSerializer},
        tags=["All"],
    ),
)
class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Product view set to get all products
    Only get method allowed
    """

    permission_classes = [permissions.AllowAny]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = ProductFilter
    filterset_fields = ["id", "category"]
    search_fields = ["name", "id"]
    ordering_fields = ["name", "rating", "overall_price", "created_at", "discount"]

    def get_queryset(self):
        if self.action == "list":
            return (
                Product.objects.prefetch_related("variants")
                .all()
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
                    price=Subquery(
                        ProductVariant.objects.filter(product=OuterRef("pk")).values(
                            "price"
                        )[:1]
                    ),
                    discount=Subquery(
                        ProductVariant.objects.filter(product=OuterRef("pk")).values(
                            "discount"
                        )[:1]
                    ),
                )
            )
        return Product.objects.all().prefetch_related("variants", "reviews")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleProductSerializer
        return ProductSerializer

    @extend_schema(
        description="Create review for product",
        request=CreateReviewSerializer,
        responses={201: ReviewSerializer},
        tags=["Product webhooks"],
    )
    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        """
        Review product
        """
        product = self.get_object()
        serializer = CreateReviewSerializer(
            data=request.data, context={"product": product, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Buy product variant",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=CreateOrderSerializer,
        responses={201: OrderSerializer},
        tags=["Product webhooks"],
    )
    @action(
        detail=True,
        methods=["post"],
    )
    @atomic
    def buy(self, request, pk=None):
        """
        Buy product variant
        """
        product_variant = ProductVariant.objects.select_for_update().get(
            pk=request.data.get("product_variant")
        )
        request.data["user"] = request.user.id
        request.data["shop"] = product_variant.product.shop.id
        serializer = CreateOrderSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    description="Product variant viewset to create product variants",
    parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
    request=CreateProductVariantSerializer,
    responses={200: ProductVariantSerializer},
    tags=["Owner"],
)
class ProductVariantViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Product variant viewset to create product variants
    Allowed create update and destroy
    """

    permission_classes = [permissions.IsAuthenticated, HasShop]

    def get_object(self):
        return ProductVariant.objects.get(pk=self.kwargs["pk"])

    @extend_schema(
        description="Create product variant attribute",
        request=CreateAttributeValueSerializer,
        responses={201: AttributeSerializer},
        tags=["Product webhooks"],
    )
    @action(detail=True, methods=["post"])
    def create_attribute_value(self, request, pk=None):
        """
        Create product variant attribute
        """
        product_variant = self.get_object()
        serializer = CreateAttributeValueSerializer(
            data=request.data,
            context={"product_variant": product_variant, "user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    tags=["Owner"],
)
class ShopProductViewSet(viewsets.ModelViewSet):
    """
    Viewset allows the owner of shop to edit products
    """

    permission_classes = [permissions.IsAuthenticated, IsOwner, HasShop]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

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
                price=Subquery(
                    ProductVariant.objects.filter(product=OuterRef("pk")).values(
                        "price"
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

    def update(self, request, *args, **kwargs):
        """
        Update product
        """
        if "cateogory" in request.data:
            product = self.get_object()
            variants = product.variants.all()
            for variant in variants:
                variant.attribute_values.all().delete()
            product.category = Category.objects.get(id=request.data["category"])
            product.save()
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        On create product set shop to user's
        """
        if self.request.user.shop is not None:
            serializer.save(shop=self.request.user.shop)  # type: ignore
        else:
            raise serializers.ValidationError("Shop not found")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CreateProductSerializer
        if self.action == "retrieve":
            return SingleProductSerializer
        return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


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


@extend_schema_view(
    list=extend_schema(
        description="Categories for products",
        responses={200: CategorySerializer},
        tags=["All"],
    ),
    retrieve=extend_schema(
        description="Category for products",
        parameters=[OpenApiParameter("slug", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses={200: SingleCategorySerializer},
        tags=["All"],
    ),
)
class CategoryViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Viewset only to get in a list Categories
    """

    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return CategorySerializer
        return SingleCategorySerializer


@extend_schema(
    description="Brands for products",
    request=BrandSerializer,
    responses={200: BrandSerializer},
    tags=["All"],
)
class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset only to get in a list Brands
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
