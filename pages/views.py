from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from .models import SiteSettings
from .serializers import SiteSettingsSerializer


class SiteSettingsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    SiteSettings viewset to get all SiteSettings
    Only get method allowed
    """

    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
