from rest_framework.permissions import BasePermission

from users.permissions import IsModerator


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.owner == request.user)


class IsLessonOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.owner == request.user)


class IsOwnerOrModerator(BasePermission):
    """Object-level: owner or moderator."""

    def has_object_permission(self, request, view, obj):
        if IsModerator().has_permission(request, view):
            return True
        owner = getattr(obj, "owner", None)
        return bool(request.user and request.user.is_authenticated and owner == request.user)









