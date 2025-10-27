from rest_framework import permissions
from users.models import User

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with role ADMIN.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == User.Role.ADMIN
        )
