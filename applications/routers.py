from rest_framework import routers

from .views import ApplicationViewSet

router = routers.SimpleRouter()

router.register("applications", ApplicationViewSet, basename="application")
