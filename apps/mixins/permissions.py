from rest_framework import permissions
from . import constants


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_staff:
            return True
        return False


class IsAgentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        groups = request.user.groups.all()
        group_name = [g.name for g in groups]
        if request.method in permissions.SAFE_METHODS:
            return True
        elif constants.USER_GROUP_AGENT in group_name:
            return True
        else:
            return False


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        groups = request.user.groups.all()
        group_name = [g.name for g in groups]
        if constants.USER_GROUP_AGENT in group_name:
            return True
        else:
            return False
