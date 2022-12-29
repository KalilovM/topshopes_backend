from rest_framework import routers
from orders.views import ShopOrderViewSet
from .views import (
    ShopViewSet,
    LinkViewSet,
)

router = routers.SimpleRouter()
# routes for authorized users
router.register(r"shop/link", LinkViewSet, basename="shop-link")
router.register(r"shop/orders", ShopOrderViewSet, basename="shop-order")
# routes for all users
router.register(r"shops", ShopViewSet, basename="shops")
