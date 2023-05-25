from django.urls import path
from . import views

urlpatterns = [
    # SYSTEM ROUTES
    path("", views.SystemListCreateView.as_view(), name = "list-cteate-system"),
    path("<int:pk>", views.SystemRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system"),

    # LISTING PARAMETER ROUTES
    path("listing-parameters/", views.ListingParameterListCreateView.as_view(), name = "list-cteate-listing-parameters"),
    path("listing-parameters/<int:pk>/", views.ListingParameterRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-listing-parameter"),
    
    # SYSTEM PARAMETER ROUTES
    path("system-parameters/", views.SystemParameterListCreateView.as_view(), name = "list-cteate-system-parameter"),
    path("system-parameters/<int:pk>/", views.SystemParameterRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-parameter"),
    
    # CURRENCY ROUTES
    path("currencies/", views.CurrencyListCreateView.as_view(), name = "list-cteate-currency"),
    path("currencies/<int:pk>/", views.CurrencyRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-currency"),

     # PAYMENT METHOD ROUTES
    path("payment-methods/", views.PaymentMethodListCreateView.as_view(), name = "list-cteate-payment-method"),
    path("payment-methods/<int:pk>/", views.PaymentMethodRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-payment-method"),
    
    # PAYMENT METHOD DISCOUNT ROUTES
    path("payment-method-discounts/", views.PaymentMethodDiscountListCreateView.as_view(), name = "list-cteate-payment-method-discount"),
    path("payment-method-discounts/<int:pk>/", views.PaymentMethodDiscountRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-payment-method-discount"),
    
    # DISCOUNT ROUTES
    path("discounts/", views.DiscountListCreateView.as_view(), name = "list-cteate-discount"),
    path("discounts/<int:pk>/", views.DiscountRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-discount"),
    
     # SERVICE SUBSCRIPTION PLAN ROUTES
    path("service-subscription-plans/", views.ServiceSubscriptionPlanListCreateView.as_view(), name = "list-cteate-service-subscription-plan"),
    path("service-subscription-plans/<int:pk>/", views.ServiceSubscriptionPlanRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-service-subscription-plan"),
    
     # SYSTEM RATING ROUTES
    path("system-ratings/", views.SystemRatingListCreateView.as_view(), name = "list-cteate-system-rating"),
    path("system-ratings/<int:pk>/", views.SystemRatingRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-rating"),
    
     # SYSTEM FEEDBACK ROUTES
    path("system-feedbacks/", views.SystemFeedbackListCreateView.as_view(), name = "list-cteate-system-feedback"),
    path("system-feedbacks/<int:pk>/", views.SystemFeedbackRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-feedback"),

    # NOTIFICATION TOPIC ROUTES
    path("notification-topics/", views.NotificationTopicListCreateView.as_view(), name = "list-cteate-notification-topic"),
    path("notification-topics/<int:pk>/", views.NotificationTopicRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-notification-topic"),
    
    # COUPON ROUTES
    path("coupons/", views.CouponListCreateView.as_view(), name = "list-cteate-coupon"),
    path("coupons/<int:pk>/", views.CouponRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-coupon"),
   
    # VOUCHER ROUTES
    path("vouchers/", views.VoucherListCreateView.as_view(), name = "list-cteate-voucher"),
    path("vouchers/<int:pk>/", views.VoucherRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-voucher"),
    
    # SUPPORTED CARD SCHEME ROUTES
    path("supported-card-schemes/", views.SupportedCardSchemeListCreateView.as_view(), name = "list-cteate-supported-card-scheme"),
    path("supported-card-schemes/<int:pk>/", views.SupportedCardSchemeRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-supported-card-scheme"),
    
    # SYSTEM ASSET OWNER ROUTES
    path("system-asset-owners/", views.SystemAssetOwnerListCreateView.as_view(), name = "list-cteate-system-asset-owner"),
    path("system-asset-owners/<int:pk>/", views.SystemAssetOwnerRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-asset-owner"),
    
    # SYSTEM ASSET ROUTES
    path("system-assets/", views.SystemAssetListCreateView.as_view(), name = "list-cteate-system-asset"),
    path("system-assets/<int:pk>/", views.SystemAssetRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-system-asset"),
    
    # REFERRAL REWARD PLAN ROUTES
    path("referral-reward-plans/", views.ReferralRewardPlanListCreateView.as_view(), name = "list-cteate-referral-reward-plan"),
    path("referral-reward-plans/<int:pk>/", views.ReferralRewardPlanRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-referral-reward-plan"),
    
    # FEATURING PRICE ROUTES
    path("featuring-prices/", views.FeaturingPriceListCreateView.as_view(), name = "list-cteate-featuring-price"),
    path("featuring-prices/<int:pk>/", views.FeaturingPriceRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-featuring-price"),
    
]

