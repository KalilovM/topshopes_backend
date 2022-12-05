from rest_framework import routers
from .views import CustomerViewSet, AddressViewSet

router = routers.SimpleRouter()

router.register(r"profile", CustomerViewSet, basename="profile")
router.register(r"address", AddressViewSet, basename="address")
