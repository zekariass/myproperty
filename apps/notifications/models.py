from django.db import models
from django.conf import settings

from apps.agents.models import Agent
from apps.system.models import NotificationTopic
from apps.mixins.common_fields import AddedOnFieldMixin


class CommonNotificationFieldsMixin(AddedOnFieldMixin):
    title = models.CharField("notification title", max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_topic = models.ForeignKey(NotificationTopic, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CommonNotificationPreferenceFieldsMixin(AddedOnFieldMixin):
    opt_in = models.BooleanField(default=True)
    notification_channel = models.CharField(max_length=30)
    notification_topic = models.ForeignKey(NotificationTopic, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserNotification(CommonNotificationFieldsMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} sent to {self.user.first_name}"


class UserNotificationPreference(CommonNotificationPreferenceFieldsMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.notification_channel}, opt_in: {self.opt_in}"


class AgentNotification(CommonNotificationFieldsMixin):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} sent to {self.agent.name}"


class AgentNotificationPreference(CommonNotificationPreferenceFieldsMixin):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.notification_channel}, opt_in: {self.opt_in}"
