from django.urls import path

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
]
