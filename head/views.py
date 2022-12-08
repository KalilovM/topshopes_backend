from rest_framework import permissions, viewsets
from shops.models import Brand, BrandType, Category, Product, Shop
from shops.serializers import BrandSerializer, BrandTypeSerializer, CategorySerializer, ProductSerializer, ShopSerializer

from users.models import Customer
from users.serializers import CustomerSerializer

class AdminUsersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class AdminBrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminBrandTypeViewSet(viewsets.ModelViewSet):
    queryset = BrandType.objects.all()
    serializer_class = BrandTypeSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related("images")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    

# class StaticPageViewSet(viewsets.ModelViewSet):
    
