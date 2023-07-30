from decimal import Decimal
from django.shortcuts import render
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.system import models as sys_models

from apps.mixins import functions, constants

from . import models as pay_models
from . import serializers as pay_serializers

from .apis import bank_transfer, voucher_payment, card_payment
from .apis.mobile_apis import mobile_payment

# from . import api as payment_api

# from apps.mixins.permissions import IsAgentOrReadOnly


def update_coupon(coupon_instance):
    sys_models.Coupon.objects.update(
        id=coupon_instance.id, use_count=F("use_count") + 1
    )


# Create your views here.
class ListCreatePaymentView(ListCreateAPIView):
    serializer_class = pay_serializers.PaymentSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = pay_models.Payment.objects.all()
            return queryset
        return []

    def post(self, request):
        with transaction.atomic():
            try:
                # GET PAYMENT DATA FROM INCOMING REQUEST DATA
                payment_data = request.data

                # GET SUB-PAYMENT DATA, SUCH AS BANK TRANSFER DATA
                sub_payment_data = request.data.pop("sub_payment")

                # CHECK IF INCOMING DATA HAS COUPON AND COUPON IS NOT NULL
                coupon_instance = None
                coupon_value = 0
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

                    #
                    if (
                        coupon_instance.discount_fixed_value <= 0
                        and coupon_instance.discount_percentage_value <= 0
                    ):
                        raise Exception(
                            f"Coupon: {coupon_instance.code} has no discount value."
                        )
                    if coupon_instance.use_count >= coupon_instance.total_use:
                        raise Exception(
                            f"Coupon: {coupon_instance.code} has been overused."
                        )
                    if coupon_instance.expire_on <= timezone.now():
                        raise Exception(
                            f"Coupon: {coupon_instance.code} has been outdated."
                        )
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

                    # sys_models.Coupon.objects.update(
                    #     id=coupon_instance.id, use_count=F("use_count") + 1
                    # )

                    # RETURN "PAYMENT SUCCESSFUL" IF COUPON HAS FULL DISCOUNT
                    # INCLUDING THE PERCENTAGE RATE AND FIXED RATE
                    if coupon_value >= payment_data["total_amount"]:
                        update_coupon(coupon_instance)
                        return Response(
                            {
                                "detail": {
                                    "message": "Payment successful",
                                    "data": "COUPON_COVERED",
                                }
                            },
                            status=status.HTTP_200_OK,
                        )
                # CALCULATE ACTUAL PAYMENT VALUE, WHICH IS AFTER COUPON VALUE IS DEDUCTED
                actual_payment_value = payment_data["total_amount"] - coupon_value

                # GENERATE UNIQUE PAYMENT ORDER NUMBER
                payment_order_number = functions.generate_payment_order_no()

                # SET THE DEFAULT CURRENCY AS CURRENCY OF PAYMENT, OTHERWISE NONE
                default_currency = (
                    sys_models.Currency.objects.filter(is_default=True).first() or None
                )

                # DESERIALISE THE PAYMENT DATA
                payment_serializer = self.get_serializer(data=payment_data)

                # CHECK IF PAYMENT DATA IS VALID, RAISE EXCEPTION OTHERWISE
                payment_serializer.is_valid(raise_exception=True)

                # SAVE MAIN PAYMENT DATA
                # try:
                payment_instance = payment_serializer.save(
                    order_no=payment_order_number,
                    currency=default_currency,
                    coupon=coupon_instance,
                )
                # except Exception as e:
                #     return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # PROCESS SUB PAYMENT DATA, SUCH AS BANK TRANSFER, CARD PAYMENT, ETC
                # CHECK THE PAYMENT METHOD AND DECIDE WICH INTERFACE TO CALL
                sub_payment_save_response = None

                if (
                    payment_instance.payment_method.name
                    == constants.PAYMENT_METHOD_BANK_TRANSFER
                ):
                    # CALL BANK TRANSFER INTERFACE
                    sub_payment_save_response = bank_transfer.bank_transfer_interface(
                        request=self.request,
                        sub_payment_data=sub_payment_data,
                        paid_amount=actual_payment_value,
                        payment=payment_instance,
                    )
                elif (
                    payment_instance.payment_method.name
                    == constants.PAYMENT_METHOD_VOUCHER
                ):
                    # CALL VOUCHER PAYMENT INTERFACE
                    sub_payment_save_response = (
                        voucher_payment.voucher_payment_interface(
                            request=self.request,
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
                    sub_payment_save_response = card_payment.card_payment_interface(
                        request=self.request,
                        sub_payment_data=sub_payment_data,
                        paid_amount=actual_payment_value,
                        payment=payment_instance,
                    )
                elif (
                    payment_instance.payment_method.name
                    == constants.PAYMENT_METHOD_MOBILE_PAYMENT
                ):
                    # CALL MOBILE PAYMENT INTERFACE
                    sub_payment_save_response = mobile_payment.mobile_payment_interface(
                        request=self.request,
                        sub_payment_data=sub_payment_data,
                        paid_amount=actual_payment_value,
                        payment=payment_instance,
                        service_provider="",
                    )

                # IF THE SUB-PAYMENT INTERFACE RETURN RESPONSE OBJECT, RETURN TO THE CLIENT DIERECTLY
                # SUB-PAYMENT INTERFACE RETURN RESPONSE OBJECT INCASE OF ERRORS
                if isinstance(sub_payment_save_response, Response):
                    return sub_payment_save_response

                # OTHERWISE SUB-PAYMENT INTERFACE RETURN TRUE/FALSE BOOLEAN.
                # TRUE INCASE OF SUCCESSFUL PAYMENT, OTHERWISE FALSE
                # RETURN RESPONSE WITH "PAYMENT SUCCESSFUL" IF TRUE IS RETURNED
                elif (
                    isinstance(sub_payment_save_response, bool)
                    and sub_payment_save_response
                ):
                    # UPDATE COUPON USE COUNT IF COUPON VALUE IS > 0
                    if coupon_value > 0:
                        update_coupon(coupon_instance)
                    return Response(
                        {
                            "detail": {
                                "message": "Payment successful",
                                "data": payment_serializer.data,
                            }
                        },
                        status=status.HTTP_200_OK,
                    )

                elif (
                    isinstance(sub_payment_save_response, bool)
                    and not sub_payment_save_response
                ):
                    # IF SUB-PAYMENT INTERFACE RETURN FALSE, THEN PAYMENT IS NOT SUCCESSFUL,
                    # SO RAISE EXCEPTION SO THAT THE WHOLE OPERTAION TO BE ROLLED BACK AS IT IS ATOMIC
                    raise Exception(
                        f"Payment with {payment_instance.payment_method.name} is not successful. Try again!"
                    )
            # RETURN ERROR IF ANY EXCEPTION IS RAISED
            except Exception as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
