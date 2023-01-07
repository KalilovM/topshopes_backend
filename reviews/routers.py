from rest_framework import routers
from .views import ReviewViewSet

router = routers.SimpleRouter()
router.register(r"reviews", ReviewViewSet, basename="review")
