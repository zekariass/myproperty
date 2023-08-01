from django.db import models
from django.conf import settings

from apps.mixins import constants

from apps.agents.models import Agent, AgentBranch
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
    # notification_channel = models.CharField(max_length=30)
    notification_topic = models.ForeignKey(NotificationTopic, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CommonNotificationChannelPreferenceFieldsMixin(AddedOnFieldMixin):
    opt_in = models.BooleanField(default=True)
    channel = models.CharField(max_length=30, choices=constants.NOTIFICATION_CHANNELS)

    class Meta:
        abstract = True


class UserNotification(CommonNotificationFieldsMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} sent to {self.user.first_name}"


class UserNotificationPreference(CommonNotificationPreferenceFieldsMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "notification_topic"],
                name="unique_user_preference_constraint",
            )
        ]

    def __str__(self) -> str:
        return f"{self.notification_topic}, opt_in: {self.opt_in}"


class UserNotificationChannelPreference(CommonNotificationChannelPreferenceFieldsMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.channel}, opt_in: {self.opt_in}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "channel"],
                name="unique_user_channel_preference_constraint",
            )
        ]


class AgentNotification(CommonNotificationFieldsMixin):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    agent_branch = models.ForeignKey(
        AgentBranch, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.title} sent to {self.agent.name}"

    def save(self, *args, **kwargs):
        if self.agent_branch.agent != self.agent:
            raise Exception(
                f"Agent Branch: {self.agent_branch} must be sub-type of Agent: {self.agent}."
            )
        super().save(*args, **kwargs)


class AgentNotificationPreference(CommonNotificationPreferenceFieldsMixin):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["agent", "notification_topic"],
                name="unique_agent_preference_constraint",
            )
        ]

    def __str__(self) -> str:
        return f"{self.notification_topic}, opt_in: {self.opt_in}"


class AgentNotificationChannelPreference(
    CommonNotificationChannelPreferenceFieldsMixin
):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["agent", "channel"],
                name="unique_agent_channel_preference_constraint",
            )
        ]

    def __str__(self) -> str:
        return f"{self.channel}, opt_in: {self.opt_in}"
