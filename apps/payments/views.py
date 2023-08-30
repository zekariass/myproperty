from decimal import Decimal
from django.shortcuts import render
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.notifications.emails import helpers

from apps.system import models as sys_models
from apps.listings import models as listing_models
from apps.agents import get_cached_or_from_db
from . import tasks

from apps.mixins.functions import get_success_response_dict, get_error_response_dict
from apps.mixins import functions, constants

from . import models as pay_models
from . import serializers as pay_serializers

from .apis import bank_transfer, voucher_payment, card_payment
from .apis.mobile_apis import mobile_payment

from apps.payments import get_cached_or_from_db as pay_get_cached_or_from_db


agent_notification_preferences = []
agent_notification_channel_preferences = []


class ListCreatePaymentView(ListCreateAPIView):
    serializer_class = pay_serializers.PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = pay_models.Payment.objects.all()
            return queryset
        return []

    def post(self, request):
        payment_data = request.data
        try:
            payment_result = perform_payment(
                self.request, self.get_serializer, payment_data
            )
        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            get_success_response_dict(data=payment_result), status=status.HTTP_200_OK
        )


def perform_payment(request, payment_serializer, payment_data, **kwargs):
    """
    Re-usable payment processing method.
    Call this method from anywhere in the application/project by passing request object, payment serializer,
    and any keyword argument
    """
    with transaction.atomic():
        try:
            # GET PAYMENT DATA FROM INCOMING REQUEST DATA
            # payment_data = request.data
            payment_data = payment_data

            # GET SUB-PAYMENT DATA, SUCH AS BANK TRANSFER DATA
            sub_payment_data = payment_data.pop("sub_payment")

            if "requested_by" not in payment_data:
                raise Exception(
                    f"'requested_by' is not proveded. Who is this payment from?"
                )

            # GET WHO IS MAKING THE PAYMENT, i.e, user, agent
            requested_by = payment_data.pop("requested_by")

            # IF PAYMENT IS REQUESTED BY AGENT
            if (
                requested_by["by"].lower()
                == constants.PAYMENT_REQUESTED_BY_AGENT.lower()
            ):
                # GET THE PAYMENT PURPOSE FROM THE INCOMING DATA
                agent_branch_id = requested_by.get("agent_branch")

                # GET THE SERVICE SUBSCRIPTION IF PAYMENT IS FOR SERVICE SUBSCRIPTION
                # service_subscription_instance = None
                # if (
                #     "service_subscription" in payment_data
                #     and payment_data["service_subscription"]
                # ):
                #     service_subscription_id = payment_data.get("service_subscription")
                #     # GET SERVICE SUBSCRIPTION FROM DB
                #     try:
                #         service_subscription_instance = (
                #             AgentServiceSubscription.objects.select_related(
                #                 "agent", "payment"
                #             ).get(id=service_subscription_id)
                #         )

                #     except:
                #         raise Exception(
                #             f"Agent Service Subscription with id {service_subscription_id} not found!"
                #         )

                # GET AGENT FROM DB
                # try:
                # agent_branch_instance = AgentBranch.objects.select_related(
                #     "agent"
                # ).get(id=agent_branch_id)
                agent_branch_instance = get_cached_or_from_db.get_agent_branch(
                    agent_branch_id
                )
                # except:
                #     raise Exception(
                #         f"Agent branch with id {agent_branch_id} not found!"
                #     )

                # GET AGENT NOTIFICATION AND CHANNEL PREFERENCES AND SET THE GLOBAL VARIABLES
                global agent_notification_preferences, agent_notification_channel_preferences
                agent_notification_channel_preferences = list(
                    helpers.get_agent_notification_channel_preferences(
                        agent_branch_instance.agent
                    )
                )
                agent_notification_preferences = list(
                    helpers.get_agent_notification_preferences(
                        agent_branch_instance.agent
                    )
                )

                # EMAIL RECIEPIENTS FOR PAYMENT ORDER AND APPROVAL CONFIRMATION
                email_recipients = []
                email_recipients.append(agent_branch_instance.email)

                # GENERATE UNIQUE PAYMENT ORDER NUMBER FOR THE PAYMENT
                payment_order_number = functions.generate_payment_order_no()

                # GET THE DEFAULT CURRENCY AS CURRENCY OF PAYMENT FROM CURRENCY TABLE, OTHERWISE NONE
                default_currency = (
                    sys_models.Currency.objects.filter(is_default=True).first() or None
                )

                # DESERIALISE THE PAYMENT DATA FOR VALIDATION
                payment_serializer = payment_serializer(data=payment_data)

                # CHECK IF PAYMENT DATA IS VALID, RAISE EXCEPTION OTHERWISE
                payment_serializer.is_valid(raise_exception=True)

                # CHECK IF INCOMING DATA HAS COUPON AND COUPON IS NOT NULL
                coupon_instance = None
                coupon_value = 0
                payment_result = None

                # DEFAULT COUPON RESULT MESSAGE
                coupon_process_result = {
                    "coupon_payment_message": None,
                    "coupon_value": coupon_value,
                    "coupon_contribution": constants.PAYMENT_COUPON_CONTRIBUTION_NONE,
                }

                # CHECK IF COUPON IS IN PAYMENT REQUEST DATA AND NOT NULL
                if "coupon" in payment_data and payment_data["coupon"] is not None:
                    # GET COUPON FROM DATABASE
                    try:
                        coupon_instance = sys_models.Coupon.objects.get(
                            id=payment_data["coupon"]
                        )
                    except:
                        raise Exception(
                            f"Coupon with id {payment_data['coupon']} does not exist."
                        )

                    # PROCESS COUPON DISCOUNT
                    coupon_process_result = process_coupon_discount(
                        request,
                        payment_data,
                        coupon_instance,
                        payment_serializer,
                        payment_order_number,
                        default_currency,
                        email_recipients,
                        agent_branch_instance,
                    )
                    # if isinstance(coupon_process_result, Response):
                    #     return coupon_process_result

                    # GET COUPON VALUE FROM PROCESSED COUPON RESULT. THE RESULT IS A DICTIONARY
                    coupon_value = coupon_process_result["coupon_value"]

                # CHECK IF COUPON CONTRIBUTION IS PARTAL OR NONE
                # PARTIAL MEANS COUPON DICOUNT COVERS PORTION OF PAYMENT
                # NONE MEANS THE AGENT HAS NO COUPON DISCOUNT
                if (
                    coupon_process_result["coupon_contribution"]
                    == constants.PAYMENT_COUPON_CONTRIBUTION_PARTIAL
                    or coupon_process_result["coupon_contribution"]
                    == constants.PAYMENT_COUPON_CONTRIBUTION_NONE
                ):
                    # CALCULATE ACTUAL PAYMENT VALUE, WHICH AFTER COUPON VALUE IS DEDUCTED
                    actual_payment_value = payment_data["total_amount"] - coupon_value

                    # SAVE MAIN PAYMENT DATA
                    payment_instance = save_main_payment(
                        payment_serializer,
                        order_no=payment_order_number,
                        currency=default_currency,
                        coupon=coupon_instance,
                    )

                    # UPDATE RELATED TABLE, SUCH AS LISTING, FOR THE PAYMENT BASED ON PAYMENT PURPOSE.
                    update_related_instance = update_related_table_based_on_payment_purpose(
                        request,
                        payment_data,
                        payment_instance=payment_instance,
                        agent_branch_instance=agent_branch_instance,
                        # service_subscription_instance=service_subscription_instance,
                    )

                    # SEND PAYMENT ORDER RECIEVED EMAIL
                    tasks.send_payment_order_recieved_email_to_agent.delay(
                        recipients=email_recipients,
                        payment_order_number=payment_instance.order_no,
                        payment_purpose=payment_data["payment_purpose"],
                        agent_branch=agent_branch_instance.id,
                        agent=agent_branch_instance.agent.id,
                        agent_notification_preferences=agent_notification_preferences,
                        agent_notification_channel_preferences=agent_notification_channel_preferences,
                        notification_topic=constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED,
                    )

                    # PROCESS SUB PAYMENT DATA, SUCH AS BANK TRANSFER, CARD PAYMENT, ETC
                    # CHECK THE PAYMENT METHOD AND DECIDE WICH INTERFACE TO CALL
                    sub_payment_saved_response = None

                    if (
                        payment_instance.payment_method.name
                        == constants.PAYMENT_METHOD_BANK_TRANSFER
                    ):
                        # CALL BANK TRANSFER INTERFACE
                        sub_payment_saved_response = (
                            bank_transfer.bank_transfer_interface(
                                request=request,
                                sub_payment_data=sub_payment_data,
                                paid_amount=actual_payment_value,
                                payment=payment_instance,
                            )
                        )
                    elif (
                        payment_instance.payment_method.name
                        == constants.PAYMENT_METHOD_VOUCHER
                    ):
                        # CALL VOUCHER PAYMENT INTERFACE
                        sub_payment_saved_response = (
                            voucher_payment.voucher_payment_interface(
                                request=request,
                                sub_payment_data=sub_payment_data,
                                paid_amount=actual_payment_value,
                                payment=payment_instance,
                            )
                        )
                    elif (
                        payment_instance.payment_method.name
                        == constants.PAYMENT_METHOD_CARD_PAYMENT
                    ):
                        # CALL CARD PAYMENT INTERFACE
                        sub_payment_saved_response = (
                            card_payment.card_payment_interface(
                                request=request,
                                sub_payment_data=sub_payment_data,
                                paid_amount=actual_payment_value,
                                payment=payment_instance,
                            )
                        )
                    elif (
                        payment_instance.payment_method.name
                        == constants.PAYMENT_METHOD_MOBILE_PAYMENT
                    ):
                        # CALL MOBILE PAYMENT INTERFACE
                        sub_payment_saved_response = (
                            mobile_payment.mobile_payment_interface(
                                request=request,
                                sub_payment_data=sub_payment_data,
                                paid_amount=actual_payment_value,
                                payment=payment_instance,
                                service_provider="",
                            )
                        )

                    # SUB-PAYMENT INTERFACE RETURN TRUE/FALSE BOOLEAN.
                    # TRUE INCASE OF SUCCESSFUL PAYMENT, OTHERWISE FALSE
                    # RETURN RESPONSE WITH "PAYMENT SUCCESSFUL" IF TRUE IS RETURNED
                    if (
                        isinstance(sub_payment_saved_response, bool)
                        and sub_payment_saved_response
                    ):
                        # UPDATE COUPON USE COUNT IF COUPON VALUE IS > 0
                        if coupon_value > 0 and coupon_instance:
                            update_coupon(coupon_instance)

                        # APPROVE THE PAYMENT IF PAYMENT IS SUCCESSFUL AND PAYMENT APPROVAL MODE OF PAYMENT METHOD IS AUTO
                        if (
                            payment_instance.payment_method.approval_mode
                            == constants.PAYMENT_APPROVAL_MODE_AUTO
                        ):
                            updated_payment_instance = approve_payment(payment_instance)

                            # UPDATE is-featured and featured_on OF LISTING, IF PAYMENT PURPOSE IS FEATURING
                            if (
                                payment_data["payment_purpose"]
                                == constants.PAYMENT_PURPOSE_FEATURING
                            ):
                                update_listing_featured_status(update_related_instance)

                            # SEND PAYMENT APPROVED EMAIL
                            tasks.send_payment_approved_email_to_agent.delay(
                                recipients=email_recipients,
                                payment_order_number=payment_instance.order_no,
                                payment_purpose=payment_data["payment_purpose"],
                                agent_branch=agent_branch_instance.id,
                                agent=agent_branch_instance.agent.id,
                                agent_notification_preferences=agent_notification_preferences,
                                agent_notification_channel_preferences=agent_notification_channel_preferences,
                                notification_topic=constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED,
                            )

                        # CREATE A SUCCESS DICTIONARY TO BE SENT TO THE CLIENT

                        # return Response(
                        #     {
                        #         "detail": {
                        #             "message": "Payment successful",
                        #             "data": payment_serializer.data,
                        #         }
                        #     },
                        #     status=status.HTTP_200_OK,
                        # )
                        payment_result = {
                            "message": "SUCCESSFUL",
                            "data": payment_serializer.data,
                            "coupon_payment": coupon_process_result,
                        }

                    elif (
                        isinstance(sub_payment_saved_response, bool)
                        and not sub_payment_saved_response
                    ):
                        # IF SUB-PAYMENT INTERFACE RETURN FALSE, THEN PAYMENT IS NOT SUCCESSFUL,
                        # SO RAISE EXCEPTION SO THAT THE WHOLE OPERTAION TO BE ROLLED BACK AS IT IS ATOMIC
                        raise Exception(
                            f"Payment with {payment_instance.payment_method.name} is not successful. Try again!"
                        )

                # CHECK IF COUPON HAS FULL PAYMENT CONTRIBUTION AND AND CONSTRUCT THE RESPONSE DICTIONARY
                if (
                    coupon_process_result["coupon_contribution"]
                    == constants.PAYMENT_COUPON_CONTRIBUTION_FULL
                ):
                    payment_result = payment_result = {
                        "message": "SUCCESSFUL",
                        "data": payment_serializer.data,
                        "coupon_payment": coupon_process_result,
                    }

                # RETURN THE RESPONSE RESULT DICTIONARY
                return payment_result

        # RETURN ERROR IF ANY EXCEPTION IS RAISED
        except Exception as e:
            raise Exception(str(e))


def update_listing_featured_status(update_related_instance):
    update_related_instance.is_featured = True
    update_related_instance.featured_on = timezone.now()
    update_related_instance.save()


def update_coupon(coupon_instance):
    sys_models.Coupon.objects.update(
        id=coupon_instance.id, use_count=F("use_count") + 1
    )


def process_coupon_discount(
    request,
    payment_data,
    coupon_instance,
    payment_serializer,
    payment_order_number,
    default_currency,
    email_recipients,
    agent_branch_instance,
):
    # payment_data = request.data
    # GET COUPON FROM DATABASE

    # CHECK COUPON VALIDITY FOR THIS PAYMENT
    if (
        coupon_instance.discount_fixed_value <= 0
        and coupon_instance.discount_percentage_value <= 0
    ):
        raise Exception(f"Coupon: {coupon_instance.code} has no discount value.")
    if coupon_instance.use_count >= coupon_instance.total_use:
        raise Exception(f"Coupon: {coupon_instance.code} has been overused.")
    if coupon_instance.expire_on <= timezone.now():
        raise Exception(f"Coupon: {coupon_instance.code} has been outdated.")
    if coupon_instance.start_on > timezone.now():
        raise Exception(
            f"Coupon: {coupon_instance.code} will be activate on {coupon_instance.start_on.date}."
        )

    # CALCULATE THE COUPON VALUE TO BE DEDUCTED FROM TOTAL_AMOUNT
    coupon_value = (
        coupon_instance.discount_percentage_value
        * Decimal(0.01)
        * payment_data["total_amount"]
        + coupon_instance.discount_fixed_value
    )

    # RETURN "PAYMENT SUCCESSFUL" IF COUPON HAS FULL DISCOUNT
    # CALCULATED FROM THE PERCENTAGE RATE AND FIXED RATE
    if coupon_value >= payment_data["total_amount"]:
        update_coupon(coupon_instance)
        # SAVE MAIN PAYMENT DATA,
        payment_instance = save_main_payment(
            payment_serializer,
            order_no=payment_order_number,
            currency=default_currency,
            coupon=coupon_instance,
        )

        updated_instance = update_related_table_based_on_payment_purpose(
            request, payment_data, payment_instance=payment_instance
        )

        # UPDATE LISTING FEATURED STATUS IF PAYMENT IS MADE FOR FEATURING AND
        # IT IS A FULLY DISCOUNTED PAYMENT
        if payment_data["payment_purpose"] == constants.PAYMENT_PURPOSE_FEATURING:
            update_listing_featured_status(updated_instance)

        # SEND PAYMENT ORDER RECIEVED EMAIL
        tasks.send_payment_order_recieved_email_to_agent.delay(
            recipients=email_recipients,
            payment_order_number=payment_instance.order_no,
            payment_purpose=payment_data["payment_purpose"],
            agent_branch=agent_branch_instance.id,
            agent=agent_branch_instance.agent.id,
            agent_notification_preferences=agent_notification_preferences,
            agent_notification_channel_preferences=agent_notification_channel_preferences,
            notification_topic=constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED,
        )

        # SEND PAYMENT APPROVED EMAIL
        tasks.send_payment_approved_email_to_agent.delay(
            recipients=email_recipients,
            payment_order_number=payment_instance.order_no,
            payment_purpose=payment_data["payment_purpose"],
            agent_branch=agent_branch_instance.id,
            agent=agent_branch_instance.agent.id,
            agent_notification_preferences=agent_notification_preferences,
            agent_notification_channel_preferences=agent_notification_channel_preferences,
            notification_topic=constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED,
        )

        # APPROVE PAYMENT SINCE IT IS FULL COUPON DISCOUTED
        approve_payment(payment_instance)

        coupon_process_result = {
            "coupon_payment_message": "SUCCESSFUL",
            "coupon_contribution": constants.PAYMENT_COUPON_CONTRIBUTION_FULL,
            "coupon_value": coupon_value,
        }

        return coupon_process_result

    coupon_process_result = {
        "coupon_payment_message": "SUCCESSFUL",
        "coupon_contribution": constants.PAYMENT_COUPON_CONTRIBUTION_PARTIAL,
        "coupon_value": coupon_value,
    }

    return coupon_process_result

    # return coupon_value


def update_related_table_based_on_payment_purpose(
    request,
    payment_data,
    payment_instance=None,
    agent_branch_instance=None,
    service_subscription_instance=None,
):
    payment_purpose = payment_data["payment_purpose"]
    updated_instance = None
    if payment_purpose == constants.PAYMENT_PURPOSE_LISTING:
        # UPDATE LISTING TABLE FOR LISTING PAYMENT
        try:
            listing_instance = listing_models.Listing.objects.get(
                id=payment_data["listing"]
            )
            listing_instance.listing_payment = payment_instance
            listing_instance.save()
        except Exception as e:
            raise Exception(
                f"Update Listing: Something went wrong when updating Listing. {str(e)}"
            )
        updated_instance = listing_instance

    elif payment_purpose == constants.PAYMENT_PURPOSE_FEATURING:
        # UPDATE LISTING TABLE FOR FEATURING PAYMENT
        try:
            listing_instance = listing_models.Listing.objects.get(
                id=payment_data["listing"]
            )
            listing_instance.featuring_payment = payment_instance
            # listing_instance.is_featured = True
            listing_instance.save()
        except Exception as e:
            raise Exception(
                f"Update Listing: Something went wrong when updating Listing, {str(e)}"
            )
        updated_instance = listing_instance

    # elif (
    #     payment_purpose == constants.PAYMENT_PURPOSE_SUBSCRIPTION
    #     and service_subscription_instance
    # ):
    #     # UPDATE AGENT SERVICE SUBSCRIPTION TABLE
    #     try:
    #         service_subscription_instance = payment_instance
    #         service_subscription_instance.save()

    #     except Exception as e:
    #         raise Exception(
    #             f"Update Service Subscription: Something went wrong when updating Agent Service Subscription. {str(e)}"
    #         )
    #     updated_instance = listing_instance
    return updated_instance


def save_main_payment(payment_serializer, **kwargs):
    payment_instance = payment_serializer.save(**kwargs)
    return payment_instance


class UnapprovedPaymentListView(ListAPIView):
    serializer_class = pay_serializers.PaymentSerializer
    permission_classes = [IsAdminUser]

    @method_decorator(cache_page(60 * 60))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def get(self, request):
        return super().get(request)

    def get_queryset(self):
        queryset = pay_models.Payment.objects.filter(is_approved=False)

        return queryset


class ApprovedPaymentListView(ListAPIView):
    serializer_class = pay_serializers.PaymentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = pay_models.Payment.objects.filter(is_approved=True)
        return queryset


class ApprovePaymentView(RetrieveUpdateDestroyAPIView):
    queryset = pay_models.Payment.objects.all()
    serializer_class = pay_serializers.PaymentSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, pk):
        # TO BE ABLE TO SEND CONFIRMATION EMAIL TO THE AGENT BRANCH, CLIENT MUST SEND AGENT BRANCH ID
        # WHICH IS ASSOCIATED WITH THE PAYMENT
        agent_branch_id = None
        if "agent_branch" in request.data:
            agent_branch_id = request.data.get("agent_branch")
        try:
            payment_instance = pay_models.Payment.objects.get(pk=pk)
            if payment_instance.is_approved:
                return Response(
                    get_success_response_dict(message="Payment already approved."),
                    status=status.HTTP_200_OK,
                )
            updated_instance = approve_payment(payment_instance)

        except Exception as e:
            return Response(
                get_error_response_dict(
                    message=f"Something went wrong when updating payment approval status. {str(e)}"
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # SEND APPROVAL CONFIRMATION EMAIL IF AGENT BRANCH IS PROVIDED
        if agent_branch_id:
            # agent_branch_instance = AgentBranch.objects.filter(id=agent_branch_id)
            agent_branch_instance = get_cached_or_from_db.get_agent_branch(
                agent_branch_id
            )

            if agent_branch_instance.exists():
                # GET AGENT NOTIFICATION AND CHANNEL PREFERENCES AND SET THE GLOBAL VARIABLES
                global agent_notification_preferences, agent_notification_channel_preferences
                agent_notification_channel_preferences = (
                    helpers.get_agent_notification_channel_preferences(
                        agent_branch_instance.agent
                    )
                )
                agent_notification_preferences = (
                    helpers.get_agent_notification_preferences(
                        agent_branch_instance.agent
                    )
                )
                email_recipient = [agent_branch_instance.email]
                tasks.send_payment_approved_email_to_agent.delay(
                    recipients=email_recipient,
                    payment_order_number=updated_instance.order_no,
                    payment_purpose=updated_instance.payment_purpose,
                    agent_branch=agent_branch_instance.id,
                    agent=agent_branch_instance.agent.id,
                    agent_notification_preferences=agent_notification_preferences,
                    agent_notification_channel_preferences=agent_notification_channel_preferences,
                    notification_topic=constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED,
                )
        return Response(
            get_success_response_dict(
                data=self.get_serializer(instance=updated_instance).data,
                message="Approved.",
            ),
            status=status.HTTP_200_OK,
        )


def approve_payment(payment_instance):
    """
    Set is_approved to True and approved_on to the current date
    """
    payment_instance.is_approved = True
    payment_instance.approved_on = timezone.now().date()
    payment_instance.save()
    return payment_instance
