from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="TopShopes API",
        default_version="v1",
        description="It's api created just for convinent using this api routes",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = (
    [
        # swagger
        re_path(
            r"^api(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^api/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        path("admin/", admin.site.urls),
        path("api/admin/",include("head.urls"), name="admin_base_API"),
        path("api/", include("users.urls"), name="users_base_API"),
        path("api/", include("orders.urls"), name="orders_base_API"),
        path("api/", include("shops.urls"), name="shops_base_API"),
        path("api/auth/login/", TokenObtainPairView.as_view(), name="token_create"),
        path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
