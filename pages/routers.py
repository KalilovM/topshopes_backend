from rest_framework import routers
from .views import SiteSettingsViewSet


router = routers.DefaultRouter()
router.register(r"settings", SiteSettingsViewSet, basename="settings")
