from django.urls import path

from orders.views import OrderItemCreateAPI, OrderViewSet


urlpatterns = [
    path("", OrderViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<uuid:pk>/",
        OrderViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("items/", OrderItemCreateAPI.as_view()),
]
