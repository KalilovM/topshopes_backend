from django.urls import include, path

from .routers import router
from .views import AdminSiteSettingsViewSet

urlpatterns = [
    path("", include(router.urls)),
    path(
        "settings/",
        AdminSiteSettingsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            }
        ),
    ),
]
