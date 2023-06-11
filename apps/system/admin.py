from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . import models as sys_models

class SystemAdmin(ModelAdmin):
    fields = ["name", "description", "added_on"]
    list_display = ["id", "name"]

admin.site.register(sys_models.System, SystemAdmin)
admin.site.register(sys_models.ListingParameter)
admin.site.register(sys_models.SystemParameter)
admin.site.register(sys_models.Currency)
admin.site.register(sys_models.PaymentMethod)
admin.site.register(sys_models.PaymentMethodDiscount)
admin.site.register(sys_models.ServiceSubscriptionPlan)
admin.site.register(sys_models.SystemRating)
admin.site.register(sys_models.SystemFeedback)
admin.site.register(sys_models.NotificationTopic)
admin.site.register(sys_models.Voucher)
admin.site.register(sys_models.Coupon)
admin.site.register(sys_models.SupportedCardScheme)
admin.site.register(sys_models.SystemAssetOwner)
admin.site.register(sys_models.SystemAsset)
admin.site.register(sys_models.ReferralRewardPlan)
admin.site.register(sys_models.FeaturingPrice)
