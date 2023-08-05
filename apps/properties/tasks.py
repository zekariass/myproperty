from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

from apps.agents import get_cached_or_from_db
from apps.mixins import constants
from apps.notifications.emails.helpers import (
    create_notification,
    get_agent_notification_channel_preferences,
    get_agent_notification_preferences,
    get_new_property_added_notification_content,
)


@shared_task
def send_new_property_added_email_to_agent(*args, **kwargs):
    agent_branch_instance = get_cached_or_from_db.get_agent_branch(
        kwargs["agent_branch"]
    )
    # GET AGENT NOTIFICATION AND CHANNEL PREFERENCES AND SET THE GLOBAL VARIABLES
    agent_notification_channel_preferences = list(
        get_agent_notification_channel_preferences(agent_branch_instance.agent)
    )
    agent_notification_preferences = list(
        get_agent_notification_preferences(agent_branch_instance.agent)
    )

    # CHECK IF AGENT HAS OPETED IN EMAIL CHANNEL PREFERENCE AND THE AGENT HAS OPTED IN THE NOTIFICATION TOPIC
    if (
        constants.NOTIFICATION_CHANNEL_EMAIL in agent_notification_channel_preferences
        and constants.NOTIFICATION_TOPIC_NEW_PROPERTY_ADDED
        in agent_notification_preferences
    ):
        context_data = {"custom_property_id": kwargs["custom_property_id"]}

        subject = f"Property {kwargs['custom_property_id']} created."

        (
            email_content,
            content_path,
            topic,
        ) = get_new_property_added_notification_content(context_data)

        send_mail(
            subject,
            "",
            settings.DEFAULT_FROM_EMAIL,
            [agent_branch_instance.email],
            html_message=email_content,
            fail_silently=True,
        )

        create_notification(
            title=subject,
            content=content_path,
            notification_topic=topic,
            agent_branch=agent_branch_instance,
            agent=agent_branch_instance.agent,
        )
