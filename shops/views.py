from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("images").all()
    serializer_class = ProductSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ShopViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == "retrieve":
            return Shop.objects.prefetch_related("products").all()
        return Shop.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleShopSerializer
        return ShopSerializer


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class BrandTypeViewSet(viewsets.ModelViewSet):
    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
