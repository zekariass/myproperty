from django.shortcuts import render
from django.db import transaction
from django.db import connection
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from apps.agents import get_cached_or_from_db
from apps.agents.tasks import send_new_service_subscription_email_to_agent
from apps.mixins import constants, custom_pagination

from apps.mixins.permissions import IsAgent
from apps.mixins.functions import get_success_response_dict, get_error_response_dict
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.payments.views import perform_payment
from apps.system.models import (
    Discount,
    ListingParameter,
    PaymentMethodDiscount,
    ServiceSubscriptionPlan,
)
from apps.system.serializers import PaymentMethodDiscountSerializer
from . import models as agent_models
from . import serializers as agent_serializers


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
        # IS REQUEST FROM A CLIENT OR NOT
        if self.request is not None:
            if self.request.method == "GET":
                return agent_serializers.AgentSerializer
            else:
                return agent_serializers.AgentCreateSerializer
        else:
            return agent_serializers.AgentCreateSerializer

    def post(self, request, *args, **kwargs):
        try:
            res = super().post(request, *args, **kwargs)
            return res
        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


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
    pagination_class = custom_pagination.GeneralCustomPagination

    def get(self, request, pk):
        try:
            agent = agent_models.Agent.objects.get(pk=pk)
        except agent_models.Agent.DoesNotExist:
            return Response(
                get_error_response_dict(message=f"No Agent found with id {pk}!"),
                status=status.HTTP_404_NOT_FOUND,
            )

        agent_branches = agent.branches.all()
        page = self.paginate_queryset(agent_branches)

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


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

        # SUPER ADMIN OF AN AGENT CAN NOT BE DELETED
        if admins.get(pk=pk).is_superadmin:
            return Response(
                get_error_response_dict(
                    message="Super admin user can not be deleted. Consider changing to non super user before deleting."
                ),
                status=status.HTTP_403_FORBIDDEN,
            )

        # IF AN AGENT HAS ONLY ONE ADMIN, AGENT ADMIN CAN NOT BE DELETED
        elif not admins.get(pk=pk).is_superadmin and admins.count() == 1:
            return Response(
                get_error_response_dict(
                    message="Operation cannot be completed. At least one admin is required!"
                ),
                status=status.HTTP_403_FORBIDDEN,
            )

        agent_models.AgentAdmin.objects.get(pk=pk).delete()
        return Response(
            get_success_response_dict(message="Admin deleted!"),
            status=status.HTTP_200_OK,
        )


class ServiceSubscriptionListCreateView(ListCreateAPIView):
    queryset = agent_models.AgentServiceSubscription.objects.all()
    serializer_class = agent_serializers.AgentServiceSubscriptionSerializer
    permission_classes = [IsAdminUser, IsAgent]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                subscription_data = request.data

                # POP PAYMENT DATA FROM SUBSCRIPTION DATA
                payment_data = subscription_data.pop("payment")

                # CHECK IF AGENT HAS ACTIVE SUBSCRIPTION ALREADY
                # IF SO RESPOND WITH CONFLICT REQUEST
                agent_has_active_subscription = (
                    agent_models.AgentServiceSubscription.objects.filter(
                        agent=subscription_data["agent"], expire_on__gte=timezone.now()
                    )
                ).exists()

                if agent_has_active_subscription:
                    return Response(
                        get_error_response_dict(
                            message="Agent has active subscription already!"
                        ),
                        status=status.HTTP_409_CONFLICT,
                    )

                # GET MAIN BRANCH OF THE AGENT
                # BECAUSE SUBSCRIPTION IS DONE AT MAIN BRANCH LEVEL
                agent_branch_instance = agent_models.AgentBranch.objects.filter(
                    is_main_branch=True, agent=subscription_data["agent"]
                ).first()

                # GET SERVICE SUBSCRIPTION PLAN WITH THE ID FROM CLIENT
                service_subscription_plan_instance = (
                    ServiceSubscriptionPlan.objects.select_related("billing_cycle").get(
                        id=subscription_data["subscription_plan"]
                    )
                )

                # CALCULATE THE EXPIRY DATE OF SUBSCRIPTION BASED ON SELECTED SUBSCRIPTION PLAN
                subscription_will_expire_on = get_subscription_expiry_on(
                    service_subscription_plan_instance
                )

                # GET SUBSCRIPTION SERIALIZER
                service_subscription_serializer = self.get_serializer(
                    data=subscription_data
                )

                # CHECK ID SUBSCRIPTION DATA IS VALID
                service_subscription_serializer.is_valid(raise_exception=True)

                # PERFORM SUBSCRIPTION PAYMENT FROM INCOMING PAYMENT DATA
                payment_result = perform_payment(
                    request, PaymentSerializer, payment_data
                )

                # GET THE PAYMENT INSTANCE ID FROM THE RETURNED PAYMENT RESULT
                payment_id = payment_result["data"]["id"]

                # GET THE PAYMENT INSTANCE FROM DB
                try:
                    payment_instance = Payment.objects.get(id=payment_id)
                except:
                    return Response(
                        get_error_response_dict(
                            message="Payment not successful or there was something wrong with saving payment data."
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # SAVE THE SERVICE SUBSCRIPTION
                service_subscription_serializer.save(
                    payment=payment_instance, expire_on=subscription_will_expire_on
                )

                # SEND SUBSCRIPTION CONFIRMATION EMAIL IF PAYMENT IS SUCCESSFUL
                if payment_instance.is_approved:
                    send_new_service_subscription_email_to_agent(
                        service_subscription_plan_id=subscription_data[
                            "subscription_plan"
                        ],
                        agent_branch=agent_branch_instance.id,
                    )

                return Response(
                    get_success_response_dict(
                        data=service_subscription_serializer.data
                    ),
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_400_BAD_REQUEST,
                )


def get_subscription_expiry_on(service_subscription_plan_instance):
    """
    Calculate service subscription expiry date from the selected service subscription plan
    """
    # GET THE BILLING CYCLE PERIODICITY FROM THE SUBSCRIPTION PLAN
    billing_cycle = service_subscription_plan_instance.billing_cycle

    # GET LENGTH OF BILLING CYCLES, I.E. 2 MONTHS, 6 MONTHS, IF THE CYCLE NAME IS SELECTED AS MONTH
    billing_cycle_length = service_subscription_plan_instance.billing_cycle_length

    # UNIT LENGTH OF PERIODICITY, SUCH AS 30 DAYS FOR A MONTH ETC.
    # FOR EXAMPLE: IF BILING CYCLE IS MONTHLY, THE UNIT MIGHT BE 30 DAYS
    periodicity_unit_length = billing_cycle.length

    # UNIT OF PERIODICITY. SUCH AS, DAY OR HOUR
    periodicity_unit = billing_cycle.length_unit

    # SET DEFAULT OF EXPIRY ON AS CURENT DATE AND TIME
    expire_on = timezone.now()

    # CALCULATE THE EXPIRE_ON VALUE BASED ON THE PERIODICITY UNIT
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


class GetPayPerListingDiscountView(APIView):
    permission_classes = [IsAgent]

    def get(self, request, pk):
        """
        Get agent Pay-Per-Listing discounts that the agent can benefit from

        # If agent is new and do not have active subscription, then can benefit from:
            ** New agent pay-per-listing discount (trackable or deadline based)
            ** Seasonal subscription discount (trackable or deadline based)
        # If agent is not new and do not have active subscription, then can benefit from:
            ** Seasonal subscription discount (trackable or deadline based)
        """
        try:
            # GET AGENT THAT THE CURRENT USER IS ASSOCIATED WITH
            user = request.user

            # DECLARE DISCOUNT VARIABLES
            new_agent_discount = None
            seasonal_discount = None

            # CHECK IF USER IS AUTHENTICATED
            if not user.is_authenticated:
                return Response(
                    get_error_response_dict(message="Sorry, you must sign first."),
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # GET THE AGENT THAT THE CURRENT USER IS ASSOCIATED WITH
            try:
                agentAdmin = agent_models.AgentAdmin.objects.select_related(
                    "agent_branch"
                ).get(user=user.id)
            except:
                return Exception("Sorry, user is not associated with any Agent.")

            # CHECK IF THE AGENT ID SENT FROM CLIENT AND THE AGENT THAT THE CURRENT USER ASSOCIATED WITH ARE SAME
            # IF NOT SAME/EQUAL RAISE EXCEPTION
            if agentAdmin.agent_branch.agent.id != pk:
                raise Exception(
                    f"Sorry, agent id {pk} is not your agent. Please provide the correct agent id."
                )

            # GET THE AGENT FROM CACHE OR DB
            try:
                agent_instance = get_cached_or_from_db.get_agent(pk)
            except ObjectDoesNotExist as e:
                raise ObjectDoesNotExist(f"No Agent found with ID {pk}")

            # CHECK IF AGENT HAS ACTIVE SUBSCRIPTION
            if agent_instance.has_active_subscription:
                return Response(
                    get_error_response_dict(
                        message=f"Agent has active subscription already."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # GET NEW AGENT PAY-PER-LISTING DISCOUNT
            active_new_agent_discount = get_new_agent_discount(
                agent_instance, constants.LISTING_PAYMENT_TYPE_PAY_PER_LISTING
            )

            # CHECK IF THE RETRIEVED NEW AGENT DISCOUNT IS NOT NULL, AND IT IS TRACKABLE AND HAS ACTION TYPE COUNT
            # PAY-PER-LISTING DISCOUNT MAY ONLY HAVE COUNT OR DEADLINE ACTION TYPES.
            # REFER THE DOCUMENT FOR THE DEFINITION
            if (
                active_new_agent_discount
                and active_new_agent_discount.is_trackable
                and active_new_agent_discount.action == constants.DISCOUNT_ACTION_COUNT
            ):
                new_agent_discount = check_and_save_discount_in_agent_discount_tracker(
                    active_new_agent_discount, agent_instance
                )

            # CHECK IF THERE IS ACTIVE NEW AGENT DISCOUNT AND NON_TRACKABLE (IF IT IS DEADLINE BASED)
            elif (
                active_new_agent_discount
                and not active_new_agent_discount.is_trackable
                and active_new_agent_discount.action
                == constants.DISCOUNT_ACTION_DEADLINE
            ):
                new_agent_discount = active_new_agent_discount

            # ======================================================================

            # CHECK IF THERE IS ACTIVE SEASONAL DISCOUNT
            active_seasonal_discount = Discount.objects.filter(
                name=constants.DISCOUNT_NAME_SEASONAL_DISCOUNT,
                expire_on__gt=timezone.now(),
                is_active=True,
                start_on__lt=timezone.now(),
                payment_type=constants.LISTING_PAYMENT_TYPE_PAY_PER_LISTING,
            ).first()

            # CHECK IF THE RETRIEVED SEASONAL DISCOUNT IS NOT NONE AND IS TRACKABLE WITH ACTION TYPE COUNT
            if (
                active_seasonal_discount
                and active_seasonal_discount.is_trackable
                and active_seasonal_discount.action == constants.DISCOUNT_ACTION_COUNT
            ):
                seasonal_discount = check_and_save_discount_in_agent_discount_tracker(
                    active_seasonal_discount, agent_instance
                )

            # CHECK IF THERE IS ACTIVE SEASONAL DISCOUNT AND NON_TRACKABLE (IF IT IS DEADLINE BASED)
            elif (
                active_seasonal_discount
                and not active_seasonal_discount.is_trackable
                and active_seasonal_discount.action
                == constants.DISCOUNT_ACTION_DEADLINE
            ):
                seasonal_discount = active_seasonal_discount

            # GET THE SUM OF ALL DISCOUNTS THAT THE AGENT IS ELIGIBLE FOR
            all_discounts = get_discount_sum(new_agent_discount, seasonal_discount)

            return Response(
                get_success_response_dict(data=all_discounts), status=status.HTTP_200_OK
            )

        # CAPTURE ANY EXCEPTION DURING THE PROCESS
        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_discount_sum(*discounts):
    """
    This function recieves list of discounts and return sum of the all discounts
    """
    all_discounts_sum = {"discount_percentage_value": 0, "discount_fixed_value": 0}
    for discount in discounts:
        if discount:
            all_discounts_sum[
                "discount_percentage_value"
            ] += discount.discount_percentage_value
            all_discounts_sum["discount_fixed_value"] += discount.discount_fixed_value
    return all_discounts_sum


def check_and_save_discount_in_agent_discount_tracker(discount, agent_instance):
    """
    This function checks and saves trackable discount in AgentDiscountTracker table

    Arguments:
        - discount: the discount object to be saved in AgentDiscountTracker
        - agent_instance: the agent object that the discount is to be tracked for
    Return:
        -Return the saved discout or None otherwise.
    """
    _discount = None

    # GET THE DISCOUNT TRACKER OBJECT IF A TRACKER HAS BEEN SAVED FOR THE AGENT FOR THIS DISCOUNT IN AgentDiscountTracker
    discount_in_tracker_for_this_agent = (
        agent_models.AgentDiscountTracker.objects.filter(
            discount=discount.id, agent=agent_instance.id, expire_on__gt=timezone.now()
        ).first()
    )

    # CHECK IF THERE IS A TRACKER FOR THE AGENT FOR THIS DISCOUNT
    # AND IF USED DISCOUNT LESS THAN MAX USE
    # ELSE, CREATE A TRACKER FOR THE AGENT FOR THIS DISCOUNT AND RETURN THE DISCOUNT
    # RETURN NULL IF TRACKER HAS BEEN CREATED ALREADY BUT ALL USED OFFERS USED OR EXPIRED
    if discount_in_tracker_for_this_agent:
        if (
            discount_in_tracker_for_this_agent.used_discounts
            < discount_in_tracker_for_this_agent.max_discounts
        ):
            _discount = discount
    else:
        # GET TRACKER LIFETIME TO SET THE EXPIRATION DATE OF THE TRACKER
        try:
            tracker_life_time = ListingParameter.objects.get(
                name=constants.LISTING_PARAM_DISCOUNT_TRACKER_LIFETIME
            )
        except:
            raise Exception(
                "DISCOUNT_TRACKER_LIFETIME must be configured in ListingParameter table."
            )

        agent_models.AgentDiscountTracker.objects.create(
            max_discounts=int(discount.value),
            used_discounts=0,
            agent=agent_instance,
            discount=discount,
            expire_on=timezone.now()
            + timezone.timedelta(days=int(tracker_life_time.value)),
            start_on=timezone.now(),
        )
        _discount = discount

    return _discount


class GetSubscriptionDiscountView(APIView):
    permission_classes = [IsAgent]

    def get(self, request, pk):
        """
        Get agent subscription discounts that the agent can benefit from

        # If agent is new, then can benefit from:
            ** New agent subscription discount
            ** Seasonal subscription discount
        # If agent is resubscribing with in resubscription grace period, then can benefit from:
            ** Resubscription discount
            ** Seasonal subscription discount
            ** Loyalty Discount
        # If agent is not new but resubscribing after resubscription grace period, then can benefit from:
            ** Seasonal subscription discount
            ** Loyalty Discount
        """
        # GET AGENT THE CURRENT USER IS ASSOCIATED WITH
        try:
            user = request.user
            new_agent_subscription_discount = None
            subscription_renewal_within_grace_period_discount = None
            seasonal_discount = None
            loyalty_discount = None

            # CHECK IF USER IS AUTHENTICATED
            if not user.is_authenticated:
                return Response(
                    get_error_response_dict(message="Sorry, you must sign first."),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                # GET THE AGENT ADMIN OBJECT THAT THE CURRENT USER IS ASSOCIATED WITH
                agentAdmin = agent_models.AgentAdmin.objects.select_related(
                    "agent_branch"
                ).get(user=user.id)
            except:
                return Response(
                    get_error_response_dict(
                        message="Sorry, user is not associated with any Agent."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # GET THE AGENT INTANE FROM THE AGENT ADMIN OBJECT
            agent_instance = agentAdmin.agent_branch.agent

            # COMPARE THE AGENT SENT FROM CLIENT AND THE AGET ASSOCIATED WITH ARE SAME
            if agent_instance.id != pk:
                return Response(
                    get_error_response_dict(
                        message=f"Sorry, agent id {pk} is not your agent. Please provide the correct agent id."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # CHECK IF AGENT HAS ACTIVE SUBSCRIPTION
            if agent_instance.has_active_subscription:
                return Response(
                    get_error_response_dict(
                        message=f"Agent has active subscription already."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # GET NEW AGENT DISCOUNT IF ANY
            new_agent_discount = get_new_agent_discount(
                agent_instance, constants.LISTING_PAYMENT_TYPE_SUBSCRIPTION
            )

            # CHECK IF new_agent_discount IS NOT NONE
            if new_agent_discount:
                if (
                    not new_agent_discount.is_trackable
                    and new_agent_discount.action == constants.DISCOUNT_ACTION_SINGLE
                    and new_agent_discount.unit == constants.DISCOUNT_UNIT_NONE
                ):
                    new_agent_subscription_discount = new_agent_discount

            # SUBSCRIPTION RENEWAL DISCOUNT

            # GET THE LAST EXPIRED SUBSCRIPTION
            # GET RESUBSCRIPTION GRACE PERIOD FROM LISTING PARAMS TABLE
            # IT IS THE TIME THAT THE AGENT CAN BENEFIT FROM OFFER IF RESUBSCRIBED
            try:
                resubscription_grace_period = ListingParameter.objects.get(
                    name=constants.LISTING_PARAM_RESUBSCRIPTION_GRACE_PERIOD
                )
            except:
                raise Exception(
                    "RESUBSCRIPTION_GRACE_PERIOD must be configured in ListingParameter table."
                )

            # CHECK IF AGENT'S LAST SUBSCRIPTION WAS EXPIRED WITHIN THE GRACE PERIOD
            last_subscription_within_grace_period = (
                agent_models.AgentServiceSubscription.objects.filter(
                    Q(
                        Q(expire_on__lte=timezone.now())
                        and Q(
                            expire_on__gt=timezone.now()
                            - timezone.timedelta(
                                days=int(resubscription_grace_period.value)
                            )
                        )
                    ),
                    agent=agent_instance.id,
                ).first()
            )

            if last_subscription_within_grace_period:
                # AGENT IS ELIGIBLE FOR RESUBSCRIPTION DISCOUNT, AND THEN CHECK FOR RESUBSCRIPTION DISCOUNT
                subscription_renewal_within_grace_period_discount = (
                    Discount.objects.filter(
                        name=constants.DISCOUNT_NAME_SUBSCRIPTION_RENEWAL_DISCOUNT,
                        expire_on__gt=timezone.now(),
                        is_active=True,
                        start_on__lt=timezone.now(),
                        payment_type=constants.LISTING_PAYMENT_TYPE_SUBSCRIPTION,
                        is_trackable=False,
                        action=constants.DISCOUNT_ACTION_SINGLE,
                        unit=constants.DISCOUNT_UNIT_NONE,
                    ).first()
                )

            # CHECK IF AGENT IS ELIGIBLE FOR LOYALTY DISCOUNT
            # GET THE LOYALTY_DISCOUNT_PRESUBSCRIPTIONS PARAM VALUE
            try:
                loyalty_presubscriptions = ListingParameter.objects.get(
                    name=constants.LISTING_PARAM_LOYALTY_DISCOUNT_PRESUBSCRIPTIONS
                )
            except:
                raise Exception(
                    "LOYALTY_DISCOUNT_PRESUBSCRIPTIONS must be configured in ListingParameter table."
                )

            # GET NUMBER OF SUBSCRIPTIONS SO FAR FOR THE AGENT
            is_illigible_for_loyalty_discount = (
                agent_models.AgentServiceSubscription.objects.filter(
                    agent=agent_instance.id
                ).count()
                >= int(loyalty_presubscriptions.value)
            )

            # CHECK IF AGENT IS ELIGIBLE FOR LOYALTY DISCOUNT
            if is_illigible_for_loyalty_discount:
                # GET LOYALTY DISCOUNT FROM DB
                loyalty_discount = Discount.objects.filter(
                    name=constants.DISCOUNT_NAME_LOYALTY_DISCOUNT,
                    expire_on__gt=timezone.now(),
                    is_active=True,
                    start_on__lt=timezone.now(),
                    payment_type=constants.LISTING_PAYMENT_TYPE_SUBSCRIPTION,
                    is_trackable=False,
                    action=constants.DISCOUNT_ACTION_SINGLE,
                    unit=constants.DISCOUNT_UNIT_NONE,
                ).first()

            # CHECK IF THERE IS SEASONAL DISCOUNT
            seasonal_discount = Discount.objects.filter(
                name=constants.DISCOUNT_NAME_SEASONAL_DISCOUNT,
                expire_on__gt=timezone.now(),
                is_active=True,
                start_on__lt=timezone.now(),
                payment_type=constants.LISTING_PAYMENT_TYPE_SUBSCRIPTION,
                is_trackable=False,
                action=constants.DISCOUNT_ACTION_SINGLE,
                unit=constants.DISCOUNT_UNIT_NONE,
            ).first()

            # SUM ALL DISCOUNTS THAT THE AGENT IS ELIGIBLE FOR
            all_discounts = get_discount_sum(
                new_agent_subscription_discount,
                subscription_renewal_within_grace_period_discount,
                seasonal_discount,
                loyalty_discount,
            )

            return Response(
                get_success_response_dict(data=all_discounts), status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_new_agent_discount(agent_instance, payment_type):
    active_new_agent_discount = None

    # GET THE NEW AGENT GRACE PERIOD PARAM FROM LISTING PARAMETER TABLE.
    # IT IS THE NUMBER OF DAYS THAT AGENT IS CONSIDERED NEW AFTER REGISTRATION
    new_agent_grace_period = ListingParameter.objects.filter(
        Q(Q(system__name="*") | Q(system__name=constants.SYSTEM_MODULE_NAME_MYPROPERY)),
        name=constants.LISTING_PARAM_NEW_AGENT_GRACE_PERIOD,
    ).first()

    if not new_agent_grace_period:
        raise Exception("NEW_AGENT_GRACE_PERIOD is not configured.")

    new_agent_grace_period_days = timezone.timedelta(
        days=int(new_agent_grace_period.value)
    )
    days_since_registered = timezone.now() - agent_instance.added_on

    # CHECK IF AGENT IS STILL IN GRACE PERIOD
    if new_agent_grace_period_days > days_since_registered:
        # AGENT IS NEW, THEN GET NEW AGENT DISCOUNT
        active_new_agent_discount = Discount.objects.filter(
            name=constants.DISCOUNT_NAME_NEW_AGENT_DISCOUNT,
            expire_on__gt=timezone.now(),
            is_active=True,
            start_on__lt=timezone.now(),
            payment_type=payment_type,
        ).first()

    return active_new_agent_discount


def update_agent_discount_tracker(agent_id):
    """
    Update agent discount tracker after listing for pay-per-listing discounts

    Arguments:
        - agent_id: agent ID that the tracker is to be updated for
    """

    # GET LIST OF UNEXPIRED AND FULLY UNUSED TRACKERS FOR THE AGENT
    agent_active_trackers = agent_models.AgentDiscountTracker.objects.select_related(
        "discount"
    ).filter(
        agent=agent_id,
        expire_on__gt=timezone.now(),
        used_discounts__lt=F("max_discounts"),
    )

    # RETURN IF NO TRACKER EXIST
    if not agent_active_trackers.exists():
        return

    # LOOP THROUGH ALL DISCOUNT TRACKERS OF THE AGENT AND UPDATE THE used_discounts VALUE
    # THEN SAVE THE TRACKER
    for tracker in agent_active_trackers:
        if tracker.discount.unit == constants.DISCOUNT_UNIT_DAY:
            diff = timezone.now() - tracker.start_on
            tracker.used_discounts = diff.days + 1
        elif tracker.discount.unit == constants.DISCOUNT_UNIT_LISTING:
            tracker.used_discounts = tracker.used_discounts + 1

        tracker.save()


class RequestListCreateView(CreateAPIView):
    queryset = agent_models.Request.objects.all()
    serializer_class = agent_serializers.RequestSerializer

    def post(self, request):
        with transaction.atomic():
            # POP CLIENT REQUEST DATA
            request_data = request.data.pop("request")

            # POP MESSAGE DATA
            request_message = request.data.pop("request_message")

            # DESERIALIZE INCOMMING DATA
            request_message_serializer = agent_serializers.RequestMessageSerializer(
                data=request_message
            )

            # CHECK IF DATA IS VALID
            request_message_serializer.is_valid(raise_exception=True)

            # IF request_id IS NONE, THAT MEANS IT IS NEW REQUEST
            if request_data["request_id"] is None:
                # POP request_id AS WE DONT NEED IT BECAUSE IT IS NEW REQUEST DATA
                request_data.pop("request_id")

                # POP REQUESTOR CLIENT DATA
                requester_data = request_data.pop("requester")

                # CHECK IF REQUIESTER IS A REGISTERED USER. IF INCOMING EMAIL ID MATCHS
                # ANY EMAIL IN DATABASE USERS, THEN IT IS A REGISTERED USER AND
                registered_user = (
                    get_user_model()
                    .objects.filter(email=requester_data["email"])
                    .first()
                )

                # DESERIALIZE THE INCOMING REQUESTER DATA FOR SAVE
                requester_serializer = agent_serializers.RequesterSerializer(
                    data=requester_data
                )

                # CHECK IF REQUESTER DATA IS VALID
                requester_serializer.is_valid(raise_exception=True)

                # DESERIALIZE REQUEST DATA FOR SAVE
                request_serializer = agent_serializers.RequestSerializer(
                    data=request_data
                )

                # CHECK IF REQUEST DATA IS VALID
                request_serializer.is_valid(raise_exception=True)

                # SAVE BOTH REQUEST AND REQUESTER DATA
                requester_instance = requester_serializer.save(user=registered_user)
                request_instance = request_serializer.save(requester=requester_instance)

            # OTHERWISE IT IS A NEW CONVERSATION MESSAGE FOR EXISTING REQUEST
            else:
                try:
                    # GET REQUEST FROM DB, OTHERWISE 404
                    request_instance = agent_models.Request.objects.get(
                        id=request_data["request_id"]
                    )
                except:
                    return Response(
                        get_error_response_dict(
                            message=f"Client Request with id {request_data['request_id']} is not found."
                        ),
                        status=status.HTTP_404_NOT_FOUND,
                    )

            # SAVE REQUEST MESSAGE
            request_message_serializer.save(request=request_instance)
            return Response(
                get_success_response_dict(data=request_message_serializer.data),
                status=status.HTTP_201_CREATED,
            )


class RequestRetrieveView(RetrieveAPIView):
    queryset = agent_models.Request.objects.all()
    serializer_class = agent_serializers.RequestSerializer

    def get(self, request, pk):
        try:
            result = agent_models.Request.objects.get(id=pk)
        except:
            return Response(
                get_error_response_dict(message=f"Request ID {pk} not found."),
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            get_success_response_dict(data=self.get_serializer(instance=result).data),
            status=status.HTTP_200_OK,
        )


class RetrieveequestByAgentRView(RetrieveAPIView):
    queryset = agent_models.Request.objects.all()
    serializer_class = agent_serializers.RequestSerializer
    permission_classes = [IsAgent]

    def get(self, request):
        agent_id = request.query_params.get("agent_branch")
        requests = agent_models.Request.objects.filter(agent_branch=agent_id)
        return Response(
            get_success_response_dict(
                data=self.get_serializer(instance=requests, many=True).data
            ),
            status=status.HTTP_200_OK,
        )
