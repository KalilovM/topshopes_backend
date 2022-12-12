from django.urls import path, include

from users.views import CustomerViewSet
from .routers import router

urlpatterns = [
    path(
        "profile/",
        CustomerViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "put": "update",
                "patch": "partial_update",
            }
        ),
        name="profile",
    ),
    path("profile/address/", include(router.urls)),
]
