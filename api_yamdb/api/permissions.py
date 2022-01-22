from rest_framework import permissions

from api_yamdb.settings import MODERATOR_ROLE, ADMINISTRATOR_ROLE


class ModeratorAdminAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in (MODERATOR_ROLE, ADMINISTRATOR_ROLE)
        )


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == ADMINISTRATOR_ROLE)


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == ADMINISTRATOR_ROLE))
