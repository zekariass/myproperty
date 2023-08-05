from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

from apps.agents import get_cached_or_from_db
from apps.mixins import constants
from apps.notifications.emails.helpers import (
    create_notification,
    get_agent_notification_channel_preferences,
    get_agent_notification_preferences,
    get_new_agent_added_email_notification_content,
    get_new_agent_branch_added_email_notification_content,
    get_new_agent_service_subscription_notification_content,
)
from apps.system.models import ServiceSubscriptionPlan


@shared_task
def send_welcome_email_to_new_agent(*args, **kwargs):
    agent_branch_instance = get_cached_or_from_db.get_agent_branch(
        kwargs["agent_branch"]
    )

    # CHECK IF AGENT HAS OPETED IN EMAIL CHANNEL PREFERENCE AND THE AGENT HAS OPTED IN THE NOTIFICATION TOPIC

    subject = f"Welcome Partner!"

    (
        email_content,
        content_path,
        topic,
    ) = get_new_agent_added_email_notification_content()

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


@shared_task
def send_new_agent_branch_added_email_to_agent(*args, **kwargs):
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
        and constants.NOTIFICATION_TOPIC_NEW_AGENT_BRANCH_ADDED
        in agent_notification_preferences
    ):
        subject = f"Agent branch {agent_branch_instance.branch_code} added"

        context_data = {"agent_branch_code": agent_branch_instance.branch_code}

        (
            email_content,
            content_path,
            topic,
        ) = get_new_agent_branch_added_email_notification_content(context_data)

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


@shared_task
def send_new_service_subscription_email_to_agent(*args, **kwargs):
    agent_branch_instance = get_cached_or_from_db.get_agent_branch(
        kwargs["agent_branch"]
    )

    service_subscription_plan = ServiceSubscriptionPlan.objects.select_related(
        "subscription_period", "billing_cycle"
    ).get(id=kwargs["service_subscription_plan_id"])

    subject = f"New Subscription Added"

    context_data = {
        "billing_cycle": service_subscription_plan.billing_cycle.name,
        "billing_cycle_length": service_subscription_plan.billing_cycle_length,
        "subscription_period": service_subscription_plan.subscription_period.name,
        "subscription_period_length": service_subscription_plan.subscription_period_length,
    }

    (
        email_content,
        content_path,
        topic,
    ) = get_new_agent_service_subscription_notification_content(context_data)

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
