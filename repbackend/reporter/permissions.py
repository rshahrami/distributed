from rest_framework import permissions

class IsAdminOrOwnProvince(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not hasattr(request.user, 'province'):
            return False
        return True