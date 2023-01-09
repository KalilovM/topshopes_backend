from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, viewsets

from .models import PageCategory, SiteSettings
from .serializers import PageCategorySerializer, SiteSettingsSerializer


@extend_schema(
    description="SiteSettings viewset to get all SiteSettings",
    responses={200: PageCategorySerializer},
    tags=["All"],
)
class PageCategoriesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Pages and categories to get only
    """

    queryset = PageCategory.objects.all().prefetch_related("pages")
    serializer_class = PageCategorySerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    description="SiteSettings viewset to get all SiteSettings",
    responses={200: SiteSettingsSerializer},
    tags=["All"],
)
class SiteSettingsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SiteSettings viewset to get all SiteSettings
    Only get method allowed
    """

    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return SiteSettings.objects.first()
