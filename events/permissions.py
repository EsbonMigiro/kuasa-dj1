from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only staff members to create events.
    """

    def has_permission(self, request, view):
        # Allow read-only access to everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow event creation only for staff members
        return request.user.is_staff
