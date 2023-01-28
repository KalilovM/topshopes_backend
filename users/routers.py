from rest_framework import routers
from .views import AddressViewSet
from payments.views import UserPaymentViewSet

router = routers.SimpleRouter()

router.register(r"address", AddressViewSet, basename="address")
router.register(r"payments", UserPaymentViewSet, basename="payment")
