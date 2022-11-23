from django.urls import include, path
from .views import AddressViewSet, CustomerViewSet


urlpatterns = [
    path(
        "",
        CustomerViewSet.as_view({"get": "list", "post": "create"}),
        name="customer-base-page",
    ),
    path(
        "<uuid:pk>/",
        CustomerViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("address/", AddressViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "address/<uuid:pk>/",
        AddressViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("orders/", include("orders.urls")),
]
