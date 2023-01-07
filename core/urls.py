from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    # swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # django admin
    path("admin/", admin.site.urls),
    # website admin's routes
    path("api/admin/", include("head.urls"), name="admin_base_API"),
    # app routes
    path("api/", include("users.urls"), name="users_base_API"),
    path("api/", include("orders.urls"), name="orders_base_API"),
    path("api/", include("products.urls"), name="products_base_API"),
    path("api/", include("reviews.urls"), name="reviews_base_API"),
    path("api/", include("shops.urls"), name="shops_base_API"),
    path("api/", include("posts.urls"), name="posts_base_API"),
    # auth routes
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_create"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # pages routes
    path("api/", include("pages.urls"), name="pages_base_API"),
    # sliders routes
    path("api/", include("sliders.urls"), name="sliders_base_API"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
