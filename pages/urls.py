from django.urls import include, path

from .routers import router
from .views import SiteSettingsViewSet

urlpatterns = [
    path(
        "settings/",
        SiteSettingsViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path("", include(router.urls)),
]
