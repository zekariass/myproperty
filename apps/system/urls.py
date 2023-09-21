from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM ROUTES
    path("", views.SystemListCreateView.as_view(), name = "list-create-system"),
    path("<int:pk>", views.SystemRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system"),

    # LISTING PARAMETER ROUTES
    path("listing-parameters/", views.ListingParameterListCreateView.as_view(), name = "list-create-listing-parameters"),
    path("listing-parameters/<int:pk>/", views.ListingParameterRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-listing-parameter"),
    
    # SYSTEM PARAMETER ROUTES
    path("system-parameters/", views.SystemParameterListCreateView.as_view(), name = "list-create-system-parameter"),
    path("system-parameters/<int:pk>/", views.SystemParameterRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-parameter"),
    
    # CURRENCY ROUTES
    path("currencies/", views.CurrencyCreateView.as_view(), name = "create-currency"),
    path("currencies/list/", views.CurrencyListView.as_view(), name = "list-currency"),
    path("currencies/<int:pk>/", views.CurrencyRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-currency"),

     # PAYMENT METHOD ROUTES
    path("payment-methods/", views.PaymentMethodCreateView.as_view(), name = "create-payment-method"),
    path("payment-methods/list/", views.PaymentMethodListView.as_view(), name = "list-payment-method"),
    path("payment-methods/<int:pk>/", views.PaymentMethodRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-payment-method"),
    
    # PAYMENT METHOD DISCOUNT ROUTES
    path("payment-method-discounts/", views.PaymentMethodDiscountCreateView.as_view(), name = "create-payment-method-discount"),
    path("payment-method-discounts/list/", views.PaymentMethodDiscountListView.as_view(), name = "list-payment-method-discount"),
    path("payment-method-discounts/<int:pk>/", views.PaymentMethodDiscountRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-payment-method-discount"),
    
    # DISCOUNT ROUTES
    path("discounts/", views.DiscountCreateView.as_view(), name = "create-discount"),
    path("discounts/list/", views.DiscountListView.as_view(), name = "list-discount"),
    path("discounts/<int:pk>/", views.DiscountRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-discount"),
    
     # SERVICE SUBSCRIPTION PLAN ROUTES
    path("service-subscription-plans/", views.ServiceSubscriptionPlanCreateView.as_view(), name = "create-service-subscription-plan"),
    path("service-subscription-plans/list/", views.ServiceSubscriptionPlanListView.as_view(), name = "list-service-subscription-plan"),
    path("service-subscription-plans/<int:pk>/", views.ServiceSubscriptionPlanRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-service-subscription-plan"),
    
     # SYSTEM RATING ROUTES
    path("system-ratings/", views.SystemRatingCreateView.as_view(), name = "create-system-rating"),
    path("system-ratings/list/", views.SystemRatingListView.as_view(), name = "list-system-rating"),
    path("system-ratings/<int:pk>/", views.SystemRatingRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-rating"),
    
     # SYSTEM FEEDBACK ROUTES
    path("system-feedbacks/", views.SystemFeedbackCreateView.as_view(), name = "create-system-feedback"),
    path("system-feedbacks/list/", views.SystemFeedbackListView.as_view(), name = "list-system-feedback"),
    path("system-feedbacks/<int:pk>/", views.SystemFeedbackRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-feedback"),

    # NOTIFICATION TOPIC ROUTES
    path("notification-topics/", views.NotificationTopicListCreateView.as_view(), name = "list-create-notification-topic"),
    path("notification-topics/<int:pk>/", views.NotificationTopicRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-notification-topic"),
    
    # COUPON ROUTES
    path("coupons/", views.CouponListCreateView.as_view(), name = "list-create-coupon"),
    path("coupons/<int:pk>/delete/", views.CouponDestroyView.as_view(), name = "destroy-coupon"),
    path("coupons/<int:pk>/", views.CouponRetrieveUpdateView.as_view(), name = "retrieve-update-coupon"),
   
    # VOUCHER ROUTES
    path("vouchers/", views.VoucherListCreateView.as_view(), name = "list-create-voucher"),
    path("vouchers/<int:pk>/delete/", views.VoucherDestroyView.as_view(), name = "destroy-voucher"),
    path("vouchers/<int:pk>/", views.VoucherRetrieveUpdateView.as_view(), name = "retrieve-update-voucher"),
    
    # SUPPORTED CARD SCHEME ROUTES
    path("supported-card-schemes/", views.SupportedCardSchemeListCreateView.as_view(), name = "list-create-supported-card-scheme"),
    path("supported-card-schemes/<int:pk>/", views.SupportedCardSchemeRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-supported-card-scheme"),
    
    # SYSTEM ASSET OWNER ROUTES
    path("system-asset-owners/", views.SystemAssetOwnerListCreateView.as_view(), name = "list-create-system-asset-owner"),
    path("system-asset-owners/list/", views.SystemAssetOwnerListView.as_view(), name = "list-system-asset-owner"),
    path("system-asset-owners/<int:pk>/", views.SystemAssetOwnerRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-asset-owner"),
    
    # SYSTEM ASSET ROUTES
    path("system-assets/", views.SystemAssetListCreateView.as_view(), name = "list-create-system-asset"),
    path("system-assets/list/", views.SystemAssetListView.as_view(), name = "list-system-asset"),
    path("system-assets/<int:pk>/", views.SystemAssetRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-asset"),
    
    # REFERRAL REWARD PLAN ROUTES
    path("referral-reward-plans/", views.ReferralRewardPlanListCreateView.as_view(), name = "list-create-referral-reward-plan"),
    path("referral-reward-plans/list/", views.ReferralRewardPlanListView.as_view(), name = "list-referral-reward-plan"),
    path("referral-reward-plans/<int:pk>/", views.ReferralRewardPlanRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-referral-reward-plan"),
    
    # FEATURING PRICE ROUTES
    path("featuring-prices/", views.FeaturingPriceListCreateView.as_view(), name = "list-create-featuring-price"),
    path("featuring-prices/", views.FeaturingPriceListView.as_view(), name = "list-featuring-price"),
    path("featuring-prices/<int:pk>/", views.FeaturingPriceRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-featuring-price"),
    
]

