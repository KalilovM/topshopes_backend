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

    message = "You don't have permission to access this shop's products"

    def has_object_permission(self, request, view, obj):
        return obj.shop == request.user.shop


class VariantOwner(permissions.BasePermission):
    """
    Check is owner
    """

    message = "You don't have permission to access this product variant"

    def has_object_permission(self, request, view, obj):
        return obj.product.shop == request.user.shop
