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
    """
    Send welcome email notification the agent when first registered to the system

    Arguments:
    - agent branch id
    """

    # GET AGENT BRANCH INTANCE THAT THE NOTIFICATION TO SEND TO
    agent_branch_instance = get_cached_or_from_db.get_agent_branch(
        kwargs["agent_branch"]
    )

    # EMAIL SUBJECT
    subject = f"Welcome Partner!"

    # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
    # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
    # BE SAVED INSTEAD OF THE CONTENT ITSELF
    (
        email_content,
        content_path,
        topic,
    ) = get_new_agent_added_email_notification_content()

    # SEND THE EMAIL NOTIFICATION
    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [agent_branch_instance.email],
        html_message=email_content,
        fail_silently=True,
    )

    # CREATE AND SAVE THE NOTIFICATION
    create_notification(
        title=subject,
        content=content_path,
        notification_topic=topic,
        agent_branch=agent_branch_instance,
        agent=agent_branch_instance.agent,
    )


@shared_task
def send_new_agent_branch_added_email_to_agent(*args, **kwargs):
    """
    Send email notification the agent branch when new agent branch is added

    Arguments:
    - agent branch id
    """

    # GET AGENT BRANCH INTANCE THAT THE NOTIFICATION TO SEND TO
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

        # CONTEXT DATA TO BE PASSED TO THE TEMPLATE
        context_data = {"agent_branch_code": agent_branch_instance.branch_code}

        # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
        # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
        # BE SAVED INSTEAD OF THE CONTENT ITSELF
        (
            email_content,
            content_path,
            topic,
        ) = get_new_agent_branch_added_email_notification_content(context_data)

        # SEND THE EMAIL
        send_mail(
            subject,
            "",
            settings.DEFAULT_FROM_EMAIL,
            [agent_branch_instance.email],
            html_message=email_content,
            fail_silently=True,
        )

        # CREATE AND SAVE THE NOTIFICATION
        create_notification(
            title=subject,
            content=content_path,
            notification_topic=topic,
            agent_branch=agent_branch_instance,
            agent=agent_branch_instance.agent,
        )


@shared_task
def send_new_service_subscription_email_to_agent(*args, **kwargs):
    """
    Sending notification to the agent for new service subscriptions

    Arguments:
    - agent_branch ID
    - service_subscription_plan_id
    """

    # GET AGENT BRANCH INTANCE THAT THE NOTIFICATION TO SEND TO
    agent_branch_instance = get_cached_or_from_db.get_agent_branch(
        kwargs["agent_branch"]
    )

    # GET THE ServiceSubscriptionPlan INSTANCE TO SEND AS CONTEXT DATA TO THE TEMPLATE
    service_subscription_plan = ServiceSubscriptionPlan.objects.select_related(
        "subscription_period", "billing_cycle"
    ).get(id=kwargs["service_subscription_plan_id"])

    subject = f"New Subscription Added"

    # CONTEXT DATA TO BE PASSED TO THE TEMPLATE
    context_data = {
        "billing_cycle": service_subscription_plan.billing_cycle.name,
        "billing_cycle_length": service_subscription_plan.billing_cycle_length,
        "subscription_period": service_subscription_plan.subscription_period.name,
        "subscription_period_length": service_subscription_plan.subscription_period_length,
    }

    # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
    # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
    # BE SAVED INSTEAD OF THE CONTENT ITSELF
    (
        email_content,
        content_path,
        topic,
    ) = get_new_agent_service_subscription_notification_content(context_data)

    # SEND THE EMAIL
    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [agent_branch_instance.email],
        html_message=email_content,
        fail_silently=True,
    )

    # CREATE AND SAVE THE NOTIFICATION
    create_notification(
        title=subject,
        content=content_path,
        notification_topic=topic,
        agent_branch=agent_branch_instance,
        agent=agent_branch_instance.agent,
    )
