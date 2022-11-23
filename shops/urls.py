from django.urls import path
from .views import (
    LinkViewSet,
    BrandTypeViewSet,
    BrandViewSet,
    CategoryViewSet,
    ProductViewSet,
    ShopViewSet,
    SizeViewSet,
    ColorViewSet,
    ReviewListAPIView,
)


urlpatterns = [
    path("", ShopViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<uuid:pk>/",
        ShopViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("products/", ProductViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "products/<uuid:pk>/",
        ProductViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("links/", LinkViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "links/<uuid:pk>/",
        LinkViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("products/brands/", BrandViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "products/brands/<uuid:pk>/",
        BrandViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path(
        "products/brands/types/",
        BrandTypeViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "products/brands/types/<uuid:pk>/",
        BrandTypeViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "products/categories/",
        CategoryViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "products/categories/<uuid:pk>/",
        CategoryViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path("products/sizes/", SizeViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "products/sizes/<uuid:pk>/",
        SizeViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("products/colors/", ColorViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "products/colors/<uuid:pk>/",
        ColorViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("products/reviews/", ReviewListAPIView.as_view()),
]
