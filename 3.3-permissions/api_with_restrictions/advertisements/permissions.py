from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Метод проверки прав на объект"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user
