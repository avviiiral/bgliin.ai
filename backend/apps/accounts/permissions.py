from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        if hasattr(request.user, "profile"):
            return request.user.profile.role == "ADMIN"

        return False