from rest_framework.permissions import BasePermission


class IsDeveloper(BasePermission):
    """
    Permission that allows access only to users in the 'Developer' group.
    """
    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="Developer").exists()
