from typing import Any
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from apps.agents import get_cached_or_from_db

from apps.agents.models import AgentAdmin, AgentBranch
from apps.properties.models import Property
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


class IsAuthorizedAgentAdmin(permissions.BasePermission):
    """
    # CHECK IF USER IS ADMIN OF CURRENT AGENT BRANCH OR MAIN BRANCH
    # ADMIN OF MAIN BRANCH CAN CREATE PROPERTY ON OTHER BRANCHES OF THE AGENT
    # BUT ADMINS OF OTHER BRANCHES OF THE AGENT CAN NOT CREATE PROPERTY FOR OTHER BRANCHES
    # OF SAME AGENT.
    """

    def has_permission(self, request, view):
        if request.method == "POST" and request.data:
            # CHECK IF CURRENT USER AND INCOMING AGENT BRANCH IS LINKED
            agent_admin_instance = AgentAdmin.objects.select_related(
                "agent_branch"
            ).filter(user=request.user.id, agent_branch=request.data["agent_branch"])

            # OTHERWISE CHECK IF USER WORKS/IS ADMIN IN MAIN BRANCH OF THE SAME AGENT
            if not agent_admin_instance.exists():
                agent_admin_instance = AgentAdmin.objects.select_related(
                    "agent_branch"
                ).filter(user=request.user.id, agent_branch__is_main_branch=True)

                agent_branch_instance = AgentBranch.objects.select_related(
                    "agent"
                ).filter(id=request.data["agent_branch"])

                if not (
                    (agent_admin_instance.exists() and agent_branch_instance.exists())
                    and (
                        agent_admin_instance.first().agent_branch.agent
                        == agent_branch_instance.first().agent
                    )
                ):
                    raise PermissionDenied(
                        "User must be admin of current agent branch or admin at main branch."
                    )

        return True


class DoesAgentOwnThisProperty(permissions.BasePermission):
    """
    # Check if the agent that current user is linked to owns the property.
    # It prevents an agent from doing any operation on other's property
    """

    def has_permission(self, request, view):
        from apps.properties.views import AgentPropertyRetrieveUpdateDestroyView
        from apps.listings.views import ListingDestroyView, ListingUpdateView
        from apps.listings.models import Listing

        # if request.method not in SAFE_METHODS:
        user_agent_branch = get_cached_or_from_db.get_user_agent_branch(request.user)
        listing_instance = None
        if "main_property" in request.data:
            property_id = request.data["main_property"]
        elif isinstance(view, AgentPropertyRetrieveUpdateDestroyView):
            property_id = view.kwargs.get("pk")
        elif isinstance(view, ListingDestroyView) or isinstance(
            view, ListingUpdateView
        ):
            listing_id = view.kwargs.get("pk")
            listing_instance = Listing.objects.select_related("main_property").get(
                id=listing_id
            )

        else:
            raise PermissionDenied("Property id not provided!")

        if listing_instance:
            property_instance = listing_instance.main_property
        else:
            property_instance = Property.objects.select_related("agent").get(
                id=property_id
            )
        property_agent_branch = property_instance.agent_branch

        if user_agent_branch != property_agent_branch:
            if not (
                user_agent_branch.is_main_branch
                and (user_agent_branch.agent == property_agent_branch.agent)
            ):
                raise PermissionDenied("Your agent does not own this property!")

        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
