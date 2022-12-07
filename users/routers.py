from rest_framework import routers
from .views import AddressViewSet

router = routers.SimpleRouter()

router.register(r"", AddressViewSet, basename="address")
