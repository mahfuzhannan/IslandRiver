from rest_framework import permissions


class RestApiPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class WebApiPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user is not None

    def has_object_permission(self, request, view, obj):
        return request.user is not None

