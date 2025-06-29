from rest_framework import permissions
from advertisements.models import Advertisement


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """Метод проверки прав на объект"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class OpenAdsLimitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == 'create' and request.data.get('status') == 'OPEN':
            return Advertisement.objects.filter(
                creator=request.user,
                status='OPEN'
            ).count() < 10
        return True