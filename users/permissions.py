from rest_framework.permissions import BasePermission


MODERATOR_GROUP = "moderators"


class IsModerator(BasePermission):
    """Checks if user is in moderators group."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name=MODERATOR_GROUP).exists()
        )


class IsSelfOrAdmin(BasePermission):
    """Allows access to self or staff."""

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or obj == request.user))










