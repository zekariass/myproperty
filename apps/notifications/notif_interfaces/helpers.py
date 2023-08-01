from apps.notifications import models as notif_models


def get_agent_notification_preferences(agent):
    """
    A helper function to list the notification preferences of the agent from DB
    """
    agent_notification_preferences = (
        notif_models.AgentNotificationPreference.objects.values_list(
            "notification_topic__name", flat=True
        ).filter(opt_in=True, agent=agent.id)
    )

    return agent_notification_preferences


def get_agent_notification_channel_preferences(agent):
    """
    A helper function to list the notification channel preferences of the agent from DB
    """
    agent_notification_channel_preferences = (
        notif_models.AgentNotificationChannelPreference.objects.values_list(
            "channel", flat=True
        ).filter(opt_in=True, agent=agent.id)
    )

    return agent_notification_channel_preferences
