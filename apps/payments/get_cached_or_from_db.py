from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from .models import Payment


def get_unapproved_payments(**kwargs):
    agent_branch_instance = cache.get(f"unapproved_payments")

    if agent_branch_instance is None:
        try:
            agent_branch_instance = Payment.objects.filter(**kwargs)
            print("==============>: HELOOOOOOOOOOOOOOOO from get_unapproved_payments")
            # print(agent_branch_instance)
            cache.set(f"unapproved_payments", agent_branch_instance, 60 * 60)
        except ObjectDoesNotExist:
            raise Exception(f"get_unapproved_payments id not found.")

    return agent_branch_instance
