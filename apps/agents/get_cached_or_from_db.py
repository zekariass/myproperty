from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from .models import Agent, AgentBranch
from apps.agents.models import AgentAdmin


def get_agent(agent_id):
    """
    Get agent from db and cache it. It needed to be cached because it is frequently accessed data
    """

    # GET CACHED AGENT IF ALREADY CACHED
    agent_instance = cache.get(f"cached_agent_{agent_id}")

    # IF NOT CACHED, THEN RETRIEVED FROM DB
    if agent_instance is None:
        try:
            agent_instance = Agent.objects.get(id=agent_id)
            cache.set(f"cached_agent_{agent_id}", agent_instance, 60)
        except ObjectDoesNotExist:
            raise Exception(f"Agent with id {agent_id} id not found.")

    return agent_instance


def get_agent_branch(agent_branch_id):
    """
    Get agent branch from db and cache it. It needed to be cached because it is frequently accessed data
    """

    # GET CACHED AGENT IF ALREADY CACHED
    agent_branch_instance = cache.get(f"cached_agent_branch_{agent_branch_id}")

    # IF NOT CACHED, THEN RETRIEVED FROM DB
    if agent_branch_instance is None:
        try:
            agent_branch_instance = AgentBranch.objects.select_related("agent").get(
                id=agent_branch_id
            )
            cache.set(
                f"cached_agent_branch_{agent_branch_id}", agent_branch_instance, 60
            )
        except ObjectDoesNotExist:
            raise Exception(f"Agent_branch with id {agent_branch_id} id not found.")

    return agent_branch_instance


def get_user_agent(user):
    cache_key = f"cached_user_agent_{user.id}"
    agent = cache.get(cache_key)
    if agent is None:
        try:
            agent_admin = AgentAdmin.objects.select_related("agent_branch__agent").get(
                user=user.id
            )

            agent = agent_admin.agent_branch.agent

            cache.set(cache_key, agent, 60 * 60)
        except:
            raise Exception(f"User with id {user.id} id not attached to any agent.")
    return agent


def get_user_agent_branch(user):
    cache_key = f"cached_user_agent_branch_{user.id}"
    agent_branch = cache.get(cache_key)
    if agent_branch is None:
        try:
            agent_admin = AgentAdmin.objects.select_related("agent_branch").get(
                user=user.id
            )

            agent_branch = agent_admin.agent_branch

            cache.set(cache_key, agent_branch, 60 * 60)
        except:
            raise Exception(f"User with id {user.id} id not attached to any agent.")
    return agent_branch
