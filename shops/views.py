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
    queryset = Product.objects.prefetch_related("images").all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ShopProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.prefetch_related("images").filter(
            shop=self.request.user.shop
        )

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop)


class MyShopViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SingleShopSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.action == "retrieve":
            return Shop.objects.prefetch_related("products").filter(
                user=self.request.user
            )
        return Shop.objects.filter(user=self.request.user.pk)


class ShopViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
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
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop)

    def get_queryset(self):
        return Link.objects.filter(shop=self.request.user.shop)


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReviewViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
