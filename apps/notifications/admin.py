from django.contrib import admin
from . import models

admin.site.register(models.UserNotification)
admin.site.register(models.AgentNotification)
admin.site.register(models.UserNotificationPreference)
admin.site.register(models.AgentNotificationPreference)
admin.site.register(models.AgentNotificationChannelPreference)
admin.site.register(models.UserNotificationChannelPreference)
