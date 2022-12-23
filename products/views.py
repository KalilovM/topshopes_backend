from rest_framework import mixins, viewsets, permissions

from products.models import (
    Size,
    Color,
    BrandType,
    Image,
    Category,
    Brand,
    Product,
    Review,
)

from products.serializers import (
    SizeSerializer,
    ColorSerializer,
    BrandSerializer,
    BrandTypeSerializer,
    ImageSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
)


class ProductViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Product viewset to get all products
    Only get method allowed
    """

    queryset = Product.objects.prefetch_related("images").all()
    serializer_class = ProductSerializer


class ShopProductViewSet(viewsets.ModelViewSet):
    """
    Viewset allows the owner of shop to edit products
    """

    serializer_class = ProductSerializer
    # Add new permission is owner
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns only current user's shop products
        """
        return Product.objects.prefetch_related("images").filter(
            shop=self.request.user.shop  # type: ignore
        )

    def perform_create(self, serializer):
        """
        On create product set shop to user's
        """
        serializer.save(shop=self.request.user.shop)  # type: ignore


class SizeViewSet(viewsets.ModelViewSet):
    """
    Size viewset every user can create own sizes for product
    """

    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ColorViewSet(viewsets.ModelViewSet):
    """
    Color viewset every user can create own color for product
    """

    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    Viewset only to get in a list Reviews
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
