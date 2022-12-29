from .routers import router
from django.urls import path, include
from .views import MyShopViewSet

urlpatterns = [
    path("", include(router.urls)),
    path(
        "shop/",
        MyShopViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "post": "create",
                "patch": "partial_update",
            }
        ),
        name="my-shop",
    ),
]
