from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsAnonymous
from .models import Customer
from rest_framework import permissions
from .serializers import CustomerSerializer


class CustomerViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = CustomerSerializer
    

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAnonymous]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        return Customer.objects.all().filter(id = self.request.user.id)
    

    
