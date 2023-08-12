from rest_framework import permissions

from apps.agents.models import AgentAdmin
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
        if request.method in permissions.SAFE_METHODS:
            return True

        agent_admin = AgentAdmin.objects.select_related("agent_branch").get(
            user=request.user
        )
        agent = agent_admin.agent_branch.agent
        group_name = agent.user_group.name

        if constants.USER_GROUP_AGENT == group_name:
            return True
        else:
            return False


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        agent_admin = AgentAdmin.objects.select_related("agent_branch").get(
            user=request.user
        )
        agent = agent_admin.agent_branch.agent
        group_name = agent.user_group.name
        if constants.USER_GROUP_AGENT == group_name:
            return True
        else:
            return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
