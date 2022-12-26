from rest_framework import routers

from orders.views import OrderItemViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"items", OrderItemViewSet, basename="orders-items")
