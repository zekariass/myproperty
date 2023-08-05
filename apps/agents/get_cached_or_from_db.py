from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from .models import Agent, AgentBranch


def get_agent(agent_id):
    cached_agent = cache.get(f"cached_agent_{agent_id}")

    if cached_agent is None:
        try:
            agent_instance = Agent.objects.get(id=agent_id)
            cache.set(f"cached_agent_{agent_id}", agent_instance, 60)
        except ObjectDoesNotExist:
            raise Exception(f"Agent with id {agent_id} id not found.")

    else:
        agent_instance = cached_agent

    return agent_instance


def get_agent_branch(agent_branch_id):
    agent_branch_instance = cache.get(f"cached_agent_branch_{agent_branch_id}")

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
