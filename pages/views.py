from rest_framework import mixins, permissions, viewsets
from .models import SiteSettings
from .serializers import SiteSettingsSerializer


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
