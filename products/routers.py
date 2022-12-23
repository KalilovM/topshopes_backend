from rest_framework import routers
from .views import (
    BrandViewSet,
    CategoryViewSet,
    ColorViewSet,
    ImageViewSet,
    ShopProductViewSet,
    ProductViewSet,
    SizeViewSet,
)

router = routers.SimpleRouter()
# routes for authorized users
router.register(r"products/sizes", SizeViewSet, basename="size")
router.register(r"products/colors", ColorViewSet, basename="color")
router.register(r"products/images", ImageViewSet, basename="image")
router.register(r"products", ShopProductViewSet, basename="product")
# routes for all users
router.register(r"shops/categories", CategoryViewSet, basename="category")
router.register(r"shops/brand", BrandViewSet, basename="brand")
router.register(r"shops/products", ProductViewSet, basename="products")
