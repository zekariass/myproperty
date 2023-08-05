from django.shortcuts import render
from django.db import transaction
from django.utils import timezone

from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from apps.agents.tasks import send_new_service_subscription_email_to_agent
from apps.mixins import constants

from apps.mixins.permissions import IsAgent
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.payments.views import perform_payment
from apps.system.models import ServiceSubscriptionPlan
from . import models as agent_models
from . import serializers as agent_serializers

from apps.mixins.functions import generate_agent_branch_code


# ====================== AGENT ====================================
# class AgentCreateView(CreateAPIView):
#     queryset = agent_models.Agent.objects.all()
#     serializer_class = agent_serializers.AgentCreateSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly,]


class AgentListCreateView(ListCreateAPIView):
    queryset = agent_models.Agent.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return agent_serializers.AgentSerializer
            else:
                return agent_serializers.AgentCreateSerializer
        else:
            return agent_serializers.AgentCreateSerializer


class AgentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = agent_models.Agent.objects.all()
    serializer_class = agent_serializers.AgentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


# ====================== AGENT BRANCH====================================
class AgentBranchListCreateView(ListCreateAPIView):
    queryset = agent_models.AgentBranch.objects.all()
    serializer_class = agent_serializers.AgentBranchSerializer

    def get(self, request, pk):
        try:
            agent = agent_models.Agent.objects.get(pk=pk)
        except agent_models.Agent.DoesNotExist:
            return Response(
                {"detail": f"No Agent found with id {pk}!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        agent_branches = agent.branches.all()
        return Response(
            {"detail": self.serializer_class(agent_branches, many=True).data},
            status=status.HTTP_200_OK,
        )


class AgentBranchRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = agent_models.AgentBranch.objects.all()
    serializer_class = agent_serializers.AgentBranchSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


# ====================== AGENT ADMIN ====================================
class AgentAdminListCreateView(ListCreateAPIView):
    # queryset = agent_models.AgentAdmin.objects.all()
    serializer_class = agent_serializers.AgentAdminSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        branch_id = self.kwargs["pk"]
        agent_admins = agent_models.AgentAdmin.objects.filter(agent_branch=branch_id)
        return agent_admins


class AgentAdminRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = agent_models.AgentAdmin.objects.all()
    serializer_class = agent_serializers.AgentAdminRetrieveUpdateDestroySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def delete(self, request, pk):
        admins = agent_models.AgentAdmin.objects.all()
        if admins.get(pk=pk).is_superadmin:
            return Response(
                {
                    "detail": "Super admin user can not be deleted. Consider changing to non super user before deleting."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif not admins.get(pk=pk).is_superadmin and admins.count() == 1:
            return Response(
                {
                    "detail": "Operation cannot be completed. At least one admin is required!"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        agent_models.AgentAdmin.objects.get(pk=pk).delete()
        return Response({"detail": "Admin deleted!"}, status=status.HTTP_200_OK)


class ServiceSubscriptionListCreateView(ListCreateAPIView):
    queryset = agent_models.AgentServiceSubscription.objects.all()
    serializer_class = agent_serializers.AgentServiceSubscriptionSerializer
    permission_classes = [IsAdminUser, IsAgent]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                subscription_data = request.data
                payment_data = subscription_data.pop("payment")

                agent_has_active_subscription = (
                    agent_models.AgentServiceSubscription.objects.filter(
                        agent=subscription_data["agent"], expire_on__gte=timezone.now()
                    )
                ).exists()

                print(
                    "++++++++============================>: ",
                    agent_has_active_subscription,
                )

                if agent_has_active_subscription:
                    return Response(
                        {"errors": "Agent has active subscription already!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                agent_branch_instance = agent_models.AgentBranch.objects.filter(
                    is_main_branch=True, agent=subscription_data["agent"]
                ).first()

                service_subscription_plan_instance = (
                    ServiceSubscriptionPlan.objects.select_related("billing_cycle").get(
                        id=subscription_data["subscription_plan"]
                    )
                )
                subscription_will_expire_on = get_subscription_expiry_on(
                    service_subscription_plan_instance
                )

                service_subscription_serializer = self.get_serializer(
                    data=subscription_data
                )
                service_subscription_serializer.is_valid(raise_exception=True)

                payment_result = perform_payment(
                    request, PaymentSerializer, payment_data
                )

                payment_id = payment_result["data"]["id"]

                try:
                    payment_instance = Payment.objects.get(id=payment_id)
                except:
                    return Response(
                        {
                            "errors": "Payment not successful or there was something wrong with saving payment data."
                        }
                    )

                service_subscription_serializer.save(
                    payment=payment_instance, expire_on=subscription_will_expire_on
                )

                if payment_instance.is_approved:
                    send_new_service_subscription_email_to_agent(
                        service_subscription_plan_id=subscription_data[
                            "subscription_plan"
                        ],
                        agent_branch=agent_branch_instance.id,
                    )

                return Response(
                    {"details": {"data": service_subscription_serializer.data}},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_subscription_expiry_on(service_subscription_plan_instance):
    billing_cycle = service_subscription_plan_instance.billing_cycle
    billing_cycle_length = service_subscription_plan_instance.billing_cycle_length

    periodicity_unit_length = billing_cycle.length
    periodicity_unit = billing_cycle.length_unit

    expire_on = timezone.now()
    if periodicity_unit == constants.PERIOD_LENGTH_UNIT_SECOND:
        expire_on = timezone.now() + (
            timezone.timedelta(seconds=periodicity_unit_length * billing_cycle_length)
        )
    elif periodicity_unit == constants.PERIOD_LENGTH_UNIT_MINUTE:
        expire_on = timezone.now() + (
            timezone.timedelta(minutes=periodicity_unit_length * billing_cycle_length)
        )
    elif periodicity_unit == constants.PERIOD_LENGTH_UNIT_HOUR:
        expire_on = timezone.now() + (
            timezone.timedelta(hours=periodicity_unit_length * billing_cycle_length)
        )
    elif periodicity_unit == constants.PERIOD_LENGTH_UNIT_DAY:
        expire_on = timezone.now() + (
            timezone.timedelta(days=periodicity_unit_length * billing_cycle_length)
        )

    return expire_on
