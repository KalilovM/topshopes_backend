from rest_framework import routers

from orders.views import OrderViewSet

router = routers.SimpleRouter()
router.register(r"orders", OrderViewSet, basename="orders")
