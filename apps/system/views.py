from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import (ListCreateAPIView, 
                                     RetrieveUpdateDestroyAPIView, 
                                     UpdateAPIView,
                                     DestroyAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     ListAPIView, 
                                     CreateAPIView)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from apps.mixins.functions import get_success_response_dict, get_error_response_dict
from apps.mixins import constants

from . import models as sys_models
from . import serializers as sys_serializers


# ================= SYSTEM ===================================
class SystemListCreateView(ListCreateAPIView):
    queryset = sys_models.System.objects.all()
    serializer_class = sys_serializers.SystemSerializer
    permission_classes = [
        IsAdminUser,
    ]


class SystemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.System.objects.all()
    serializer_class = sys_serializers.SystemSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== LISTING PARAMETER ============================
class ListingParameterListCreateView(ListCreateAPIView):
    queryset = sys_models.ListingParameter.objects.all()
    serializer_class = sys_serializers.ListingParameterSerializer
    permission_classes = [
        IsAdminUser,
    ]


class ListingParameterRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.ListingParameter.objects.all()
    serializer_class = sys_serializers.ListingParameterSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== SYSTEM PARAMETER ============================
class SystemParameterListCreateView(ListCreateAPIView):
    queryset = sys_models.SystemParameter.objects.all()
    serializer_class = sys_serializers.SystemParameterSerializer
    permission_classes = [
        IsAdminUser,
    ]


class SystemParameterRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.SystemParameter.objects.all()
    serializer_class = sys_serializers.SystemParameterSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== CURRENCY ======================================
class CurrencyCreateView(CreateAPIView):
    queryset = sys_models.Currency.objects.all()
    serializer_class = sys_serializers.CurrencySerializer
    permission_classes = [
        IsAdminUser,
    ]

class CurrencyListView(ListAPIView):
    queryset = sys_models.Currency.objects.all()
    serializer_class = sys_serializers.CurrencySerializer
    

class CurrencyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.Currency.objects.all()
    serializer_class = sys_serializers.CurrencySerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== PAYMENT METHOD ======================================
class PaymentMethodCreateView(CreateAPIView):
    queryset = sys_models.PaymentMethod.objects.all()
    serializer_class = sys_serializers.PaymentMethodSerializer
    permission_classes = [
        IsAdminUser,
    ]

class PaymentMethodListView(ListAPIView):
    queryset = sys_models.PaymentMethod.objects.all()
    serializer_class = sys_serializers.PaymentMethodSerializer
    

class PaymentMethodRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.PaymentMethod.objects.all()
    serializer_class = sys_serializers.PaymentMethodSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== PAYMENT METHOD DISCOUNT ===============================
class PaymentMethodDiscountCreateView(CreateAPIView):
    queryset = sys_models.PaymentMethodDiscount.objects.all()
    serializer_class = sys_serializers.PaymentMethodDiscountSerializer
    permission_classes = [
        IsAdminUser,
    ]

class PaymentMethodDiscountListView(ListAPIView):
    queryset = sys_models.PaymentMethodDiscount.objects.all()
    serializer_class = sys_serializers.PaymentMethodDiscountSerializer
    


class PaymentMethodDiscountRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.PaymentMethodDiscount.objects.all()
    serializer_class = sys_serializers.PaymentMethodDiscountSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== DISCOUNTS ==============================================
class DiscountCreateView(CreateAPIView):
    queryset = sys_models.Discount.objects.all()
    serializer_class = sys_serializers.DiscountSerializer
    permission_classes = [
        IsAdminUser,
    ]

class DiscountListView(ListAPIView):
    queryset = sys_models.Discount.objects.all()
    serializer_class = sys_serializers.DiscountSerializer


class DiscountRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.Discount.objects.all()
    serializer_class = sys_serializers.DiscountSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== SERVICE SUBSCRIPTION PLAN ==============================================
class ServiceSubscriptionPlanCreateView(CreateAPIView):
    queryset = sys_models.ServiceSubscriptionPlan.objects.all()
    serializer_class = sys_serializers.ServiceSubscriptionPlanSerializer
    permission_classes = [
        IsAdminUser,
    ]

class ServiceSubscriptionPlanListView(ListAPIView):
    queryset = sys_models.ServiceSubscriptionPlan.objects.all()
    serializer_class = sys_serializers.ServiceSubscriptionPlanSerializer


class ServiceSubscriptionPlanRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.ServiceSubscriptionPlan.objects.all()
    serializer_class = sys_serializers.ServiceSubscriptionPlanSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== SYSTEM RATING ==============================================
class SystemRatingCreateView(CreateAPIView):
    queryset = sys_models.SystemRating.objects.all()
    serializer_class = sys_serializers.SystemRatingSerializer
    permission_classes = [
        IsAdminUser,
    ]

class SystemRatingListView(ListAPIView):
    queryset = sys_models.SystemRating.objects.all()
    serializer_class = sys_serializers.SystemRatingSerializer


class SystemRatingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.SystemRating.objects.all()
    serializer_class = sys_serializers.SystemRatingSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== SYSTEM FEEDBACK ==============================================
class SystemFeedbackCreateView(CreateAPIView):
    queryset = sys_models.SystemFeedback.objects.all()
    serializer_class = sys_serializers.SystemFeedbackSerializer
    permission_classes = [
        IsAdminUser,
    ]

class SystemFeedbackListView(ListAPIView):
    queryset = sys_models.SystemFeedback.objects.all()
    serializer_class = sys_serializers.SystemFeedbackSerializer
    


class SystemFeedbackRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.SystemFeedback.objects.all()
    serializer_class = sys_serializers.SystemFeedbackSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== NOTIFICATION TOPIC ==============================================
class NotificationTopicListCreateView(ListCreateAPIView):
    queryset = sys_models.NotificationTopic.objects.all()
    serializer_class = sys_serializers.NotificationTopicSerializer
    permission_classes = [
        IsAdminUser,
    ]


class NotificationTopicRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.NotificationTopic.objects.all()
    serializer_class = sys_serializers.NotificationTopicSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== COUPON ==============================================
class CouponListCreateView(ListCreateAPIView):
    queryset = sys_models.Coupon.objects.all()
    serializer_class = sys_serializers.CouponSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        try:
            coupon_life_time = int(
                sys_models.SystemParameter.objects.filter(
                    name=constants.SYSTEM_PARAM_COUPON_LIFE_TIME
                )
                .first()
                .value
            )
        except:
            return Response(
                get_error_response_dict(
                    message=f"No Coupon life time system parameter with name {constants.SYSTEM_PARAM_VOUCHER_LIFE_TIME} found. Add the parameter."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        coupon_serializer = self.get_serializer(data=request.data)
        coupon_serializer.is_valid(raise_excepton=True)
        coupon_serializer.save(expire_on=timezone.now() + timedelta(coupon_life_time))


class CouponDestroyView(DestroyAPIView):
    queryset = sys_models.Coupon.objects.all()
    serializer_class = sys_serializers.CouponSerializer
    permission_classes = [
        IsAdminUser,
    ]


class CouponRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = sys_models.Coupon.objects.all()
    serializer_class = sys_serializers.CouponSerializer


# ============== VOUCHER ==============================================
class VoucherListCreateView(ListCreateAPIView):
    queryset = sys_models.Voucher.objects.all()
    serializer_class = sys_serializers.VoucherSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        try:
            voucher_life_time = int(
                sys_models.SystemParameter.objects.filter(
                    name=constants.SYSTEM_PARAM_VOUCHER_LIFE_TIME
                )
                .first()
                .value
            )
        except:
            return Response(
                get_error_response_dict(
                    message=f"No voucher life time system parameter with name {constants.SYSTEM_PARAM_VOUCHER_LIFE_TIME} found. Add the parameter."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        voucher_serializer = self.get_serializer(data=request.data)
        voucher_serializer.is_valid(raise_excepton=True)
        voucher_serializer.save(expire_on=timezone.now() + timedelta(voucher_life_time))


class VoucherDestroyView(DestroyAPIView):
    queryset = sys_models.Voucher.objects.all()
    serializer_class = sys_serializers.VoucherSerializer

class VoucherRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = sys_models.Voucher.objects.all()
    serializer_class = sys_serializers.VoucherSerializer


# ============== SUPPORTED CARD SCHEME ===================================
class SupportedCardSchemeListCreateView(ListCreateAPIView):
    queryset = sys_models.SupportedCardScheme.objects.all()
    serializer_class = sys_serializers.SupportedCardSchemeSerializer
    permission_classes = [
        IsAdminUser,
    ]


class SupportedCardSchemeListView(ListAPIView):
    queryset = sys_models.SupportedCardScheme.objects.all()
    serializer_class = sys_serializers.SupportedCardSchemeSerializer
    

class SupportedCardSchemeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.SupportedCardScheme.objects.all()
    serializer_class = sys_serializers.SupportedCardSchemeSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== SYSTEM ASSET OWNER ===================================
class SystemAssetOwnerListCreateView(ListCreateAPIView):
    queryset = sys_models.SystemAssetOwner.objects.all()
    serializer_class = sys_serializers.SystemAssetOwnerSerializer
    permission_classes = [
        IsAdminUser,
    ]


class SystemAssetOwnerListView(ListAPIView):
    queryset = sys_models.SystemAssetOwner.objects.all()
    serializer_class = sys_serializers.SystemAssetOwnerSerializer


class SystemAssetOwnerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.SystemAssetOwner.objects.all()
    serializer_class = sys_serializers.SystemAssetOwnerSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== SYSTEM ASSET ===================================
class SystemAssetListCreateView(ListCreateAPIView):
    queryset = sys_models.SystemAsset.objects.all()
    serializer_class = sys_serializers.SystemAssetSerializer
    permission_classes = [
        IsAdminUser,
    ]


class SystemAssetListView(ListAPIView):
    queryset = sys_models.SystemAsset.objects.all()
    serializer_class = sys_serializers.SystemAssetSerializer
    


class SystemAssetRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.SystemAsset.objects.all()
    serializer_class = sys_serializers.SystemAssetSerializer
    permission_classes = [
        IsAdminUser,
    ]


# ============== REFERRAL REWARD PLAN ===================================
class ReferralRewardPlanListCreateView(ListCreateAPIView):
    queryset = sys_models.ReferralRewardPlan.objects.all()
    serializer_class = sys_serializers.ReferralRewardPlanSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request):
        reward_plan_serializer = self.serializer_class(data=request.data)

        if reward_plan_serializer.is_valid():
            try:
                reward_plan_serializer.save()
            except ValueError:
                # CAPTURE IF UNEXPIRED PLAN IS ALREADY EXIST FOR A SYSTEM MODULE
                return Response(
                    get_error_response_dict(
                        message="A system module can only have one unexpired reward plan."
                    ),
                    status=status.HTTP_409_CONFLICT,
                )
            return Response(
                get_success_response_dict(data=reward_plan_serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(message="Data is invalid!"),
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReferralRewardPlanListView(ListAPIView):
    queryset = sys_models.ReferralRewardPlan.objects.all()
    serializer_class = sys_serializers.ReferralRewardPlanSerializer


class ReferralRewardPlanRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.ReferralRewardPlan.objects.all()
    serializer_class = sys_serializers.ReferralRewardPlanSerializer
    permission_classes = [
        IsAdminUser,
    ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        reward_plan_serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )

        if reward_plan_serializer.is_valid():
            try:
                reward_plan_serializer.save()
            except Exception as e:
                # CAPTURE IF UNEXPIRED PLAN IS ALREADY EXIST FOR A SYSTEM MODULE
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_409_CONFLICT,
                )
            return Response(
                get_success_response_dict(data=reward_plan_serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(message="Data is not valid!"),
                status=status.HTTP_400_BAD_REQUEST,
            )


# ============== FEATURING PRICE ========================================
class FeaturingPriceListCreateView(ListCreateAPIView):
    queryset = sys_models.FeaturingPrice.objects.all()
    serializer_class = sys_serializers.FeaturingPriceSerializer
    permission_classes = [
        IsAdminUser,
    ]

class FeaturingPriceListView(ListAPIView):
    queryset = sys_models.FeaturingPrice.objects.all()
    serializer_class = sys_serializers.FeaturingPriceSerializer


class FeaturingPriceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = sys_models.FeaturingPrice.objects.all()
    serializer_class = sys_serializers.FeaturingPriceSerializer
    permission_classes = [
        IsAdminUser,
    ]
