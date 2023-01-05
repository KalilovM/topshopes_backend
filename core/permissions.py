from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    """
    Check anonymous users
    """

    def has_permission(self, request, view):
        return request.user.is_anonymous


class HasShop(permissions.BasePermission):
    """
    Check has shop
    """

    message = "You don't have shop"

    def has_permission(self, request, view):
        return hasattr(request.user, "shop")


class IsOwner(permissions.BasePermission):
    """
    Check is owner
    """

    def has_object_permission(self, request, view, obj):
        return obj.shop == request.user.shop
