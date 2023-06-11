from django.contrib import admin

from . import models


admin.site.register(models.Agent)
admin.site.register(models.AgentBranch)
admin.site.register(models.AgentAdmin)
admin.site.register(models.AgentDiscountTracker)
admin.site.register(models.AgentServiceSubscription)
admin.site.register(models.AgentReferralTracker)
admin.site.register(models.AgentReferral)
admin.site.register(models.AgentReferralReward)
admin.site.register(models.Requester)
admin.site.register(models.Request)
admin.site.register(models.RequestMessage)