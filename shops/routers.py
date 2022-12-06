from rest_framework import routers
from orders.views import ShopOrderViewSet
from .views import (
    BrandViewSet,
    CategoryViewSet,
    ColorViewSet,
    ImageViewSet,
    MyShopViewSet,
    ShopProductViewSet,
    ShopViewSet,
    ProductViewSet,
    SizeViewSet,
    LinkViewSet,
)

router = routers.SimpleRouter()
router.register(r"shops/products/categories", CategoryViewSet, basename="category")
router.register(r"shops/products/brand", BrandViewSet, basename="brand")
router.register(r"shops/porducts/images", ImageViewSet, basename="image")
router.register(r"shops/products/sizes", SizeViewSet, basename="size")
router.register(r"shops/products/colors", ColorViewSet, basename="color")
router.register(r"products", ShopProductViewSet, basename="product")
router.register(r"shop/orders", ShopOrderViewSet, basename="shop-order")
router.register(r"shop/link", LinkViewSet, basename="shop-link")
router.register(r"shop", MyShopViewSet, basename="shop")

router.register(r"shops", ShopViewSet, basename="shops")
router.register(r"shops/products",ProductViewSet, basename="products")
