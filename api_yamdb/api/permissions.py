from rest_framework import permissions


class ModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in ('moderator', 'admin')
        )


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin')
