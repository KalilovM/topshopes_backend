from rest_framework import routers
from orders.views import ShopOrderViewSet
from .views import BrandViewSet, CategoryViewSet, ColorViewSet, ImageViewSet, ShopViewSet, ProductViewSet, SizeViewSet

router = routers.SimpleRouter()
router.register(r"shop", ShopViewSet, basename="shop")
router.register(r"products/categories", CategoryViewSet, basename="category")
router.register(r"products/brand", BrandViewSet, basename="brand")
router.register(r"porducts/images", ImageViewSet, basename="image")
router.register(r"products/sizes", SizeViewSet, basename="size")
router.register(r"products/colors", ColorViewSet, basename="color")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"shop/orders", ShopOrderViewSet, basename="shop-order")

