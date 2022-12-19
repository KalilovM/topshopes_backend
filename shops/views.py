from rest_framework import mixins, permissions, viewsets
from .models import (
    Link,
    Shop,
    Size,
    Color,
    BrandType,
    Image,
    Category,
    Brand,
    Product,
    Review,
)
from .serializers import (
    LinkSerializer,
    ShopSerializer,
    SingleShopSerializer,
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
            shop=self.request.user.shop
        )

    def perform_create(self, serializer):
        """
        On create product set shop to user's
        """
        serializer.save(shop=self.request.user.shop)


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
