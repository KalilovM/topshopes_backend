from rest_framework import routers
from .views import (
    BrandViewSet,
    CategoryViewSet,
    ImageViewSet,
    ShopProductViewSet,
    ProductViewSet,
    ProductVariantViewSet,
)

router = routers.SimpleRouter()
# routes for authorized users
router.register(r"products/variants/images", ImageViewSet, basename="image")
router.register(r"products/variants", ProductVariantViewSet, basename="variant")
router.register(r"products", ShopProductViewSet, basename="product")
# routes for all users
router.register(r"shops/categories", CategoryViewSet, basename="category")
router.register(r"shops/brand", BrandViewSet, basename="brand")
router.register(r"shops/products", ProductViewSet, basename="products")
