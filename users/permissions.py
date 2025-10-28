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

class IsStudent(permissions.BasePermission):
    """
    Custom permission to allow access only to users with the STUDENT role.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role == User.Role.STUDENT
    
class IsAdminOrStudent(permissions.BasePermission):
    """
    Custom permission to allow access only to users with the ADMIN or STUDENT role.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in [User.Role.ADMIN, User.Role.STUDENT]