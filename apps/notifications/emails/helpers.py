from django.core.cache import cache

from apps.notifications import models as notif_models
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.mixins import constants

from apps.system.models import NotificationTopic


def send_email(*args, **kwargs):
    send_mail(*args, **kwargs)


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


def get_payment_order_confirmation_email_content(payment_purpose, context_data={}):
    """
    Get the right content for the specific payment order notification.
    the notification depends on the payment purpose.
    """

    # ACTUAL EMAIL CONTENT TO BE READ FROM FILE
    email_content = None

    # THE CONTENT FILE PATH TO BE SAVED IN DB
    content_path = None

    # TOPIC OF THE EMAIL NOTIFICATION TO BE READ FROM CONSTANTS MODULE
    # topic = None
    # if payment_purpose == constants.PAYMENT_PURPOSE_FEATURING:
    #     content_path = "emails/featuring_payment_requested.html"
    # elif payment_purpose == constants.PAYMENT_PURPOSE_LISTING:
    #     content_path = "emails/listing_payment_requested.html"
    # elif payment_purpose == constants.PAYMENT_PURPOSE_SUBSCRIPTION:
    #     content_path = "emails/new_service_subscription.html"
    # else:
    #     email_content = ""
    content_path = "emails/payment_requested.html"
    context_data = {**context_data, "payment_purpose": payment_purpose, **context_data}
    topic = get_notification_topic(constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED)
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_payment_approval_confirmation_email_content(payment_purpose, context_data={}):
    """
    Get the right content for the specific payment approval notification.
    the notification depends on the payment purpose.
    """

    # ACTUAL EMAIL CONTENT TO BE READ FROM FILE
    email_content = None

    # THE CONTENT FILE PATH TO BE SAVED IN DB
    content_path = None

    # TOPIC OF THE EMAIL NOTIFICATION TO BE READ FROM CONSTANTS MODULE
    topic = None
    # if payment_purpose == constants.PAYMENT_PURPOSE_FEATURING:
    #     content_path = "emails/featuring_payment_approved.html"

    # elif payment_purpose == constants.PAYMENT_PURPOSE_LISTING:
    #     content_path = "emails/listing_payment_approved.html"
    # elif payment_purpose == constants.PAYMENT_PURPOSE_SUBSCRIPTION:
    #     content_path = "emails/new_service_subscription.html"
    # else:
    #     email_content = ""

    content_path = "emails/payment_approved.html"
    context_data = {**context_data, "payment_purpose": payment_purpose, **context_data}
    topic = get_notification_topic(constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED)
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_new_property_added_notification_content(context_data=None):
    topic = get_notification_topic(constants.NOTIFICATION_TOPIC_NEW_PROPERTY_ADDED)
    content_path = "emails/new_property_added.html"
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_new_agent_added_email_notification_content(context_data=None):
    topic = get_notification_topic(constants.NOTIFICATION_TOPIC_NEW_AGENT_ADDED)
    content_path = "emails/new_agent_added.html"
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_new_agent_service_subscription_notification_content(context_data=None):
    topic = get_notification_topic(
        constants.NOTIFICATION_TOPIC_NEW_AGENT_SERVICE_SUBSCRIPTION
    )
    content_path = "emails/new_service_subscription_added.html"
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_new_agent_branch_added_email_notification_content(context_data=None):
    topic = get_notification_topic(constants.NOTIFICATION_TOPIC_NEW_AGENT_BRANCH_ADDED)
    content_path = "emails/new_agent_branch_added.html"
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_new_listing_added_notification_content(context_data=None):
    topic = get_notification_topic(constants.NOTIFICATION_TOPIC_NEW_LISTING_ADDED)
    content_path = "emails/new_listing_added.html"
    email_content = render_to_string(content_path, context_data)
    return (email_content, content_path, topic)


def get_notification_topic(topic_name):
    # Get notification topic from the database
    try:
        topic = NotificationTopic.objects.get(name=topic_name)
    except Exception as e:
        raise Exception(f"File: {__file__}, function: get_notification_topic: {str(e)}")
    return topic


def create_notification(**kwargs):
    """
    Create the notifiocation and save to DB

    Keyword Arguments:

        title,
        content,
        notification_topic,
        agent_branch,
        agent,
    """
    try:
        notif_models.AgentNotification.objects.create(**kwargs)
    except Exception as e:
        raise Exception(f"File: {__file__} function: create_notification: {str(e)}")
