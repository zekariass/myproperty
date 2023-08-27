# from base.celery import app
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from apps.agents import get_cached_or_from_db

from apps.mixins import constants
from apps.notifications.emails import helpers


@shared_task
def send_payment_order_recieved_email_to_agent(*args, **kwargs):
    """
    This function handles the sending of email notification to agent as the payment order is recieved.
     Arguments:
        recipients,
        payment_order_number,
        payment_purpose,
        agent_branch,
        agent,
        agent_notification_preferences,
        agent_notification_channel_preferences,
        notification_topic,
    """

    # CHECK IF AGENT HAS OPETED IN EMAIL CHANNEL PREFERENCE AND THE AGENT HAS OPTED IN THE NOTIFICATION TOPIC
    if (
        constants.NOTIFICATION_CHANNEL_EMAIL
        in kwargs["agent_notification_channel_preferences"]
        and kwargs["notification_topic"] in kwargs["agent_notification_preferences"]
    ):
        subject = "New Payment Order"

        context_data = {
            "po_number": kwargs["payment_order_number"],
        }

        # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
        # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
        # BE SAVED INSTEAD OF THE CONTENT ITSELF
        (
            email_content,
            content_path,
            topic,
        ) = helpers.get_payment_order_confirmation_email_content(
            kwargs["payment_purpose"], context_data
        )

        # SEND THE EMAIL TO THE AGENT
        send_mail(
            subject,
            "",
            settings.DEFAULT_FROM_EMAIL,
            kwargs["recipients"],
            html_message=email_content,
            fail_silently=True,
        )

        agent_branch_instance = get_cached_or_from_db.get_agent_branch(
            kwargs["agent_branch"]
        )

        # CALL create_agent_notification TO CREATE AND SAVE THE NOTIFICATION
        helpers.create_agent_notification(
            title=subject,
            content=content_path,
            notification_topic=topic,
            agent_branch=agent_branch_instance,
            agent=agent_branch_instance.agent,
        )


@shared_task
def send_payment_approved_email_to_agent(*args, **kwargs):
    """
    Send payment approval confirmation email after the payment is approved by admin

    Arguments:
        recipients,
        payment_order_number,
        payment_purpose,
        agent_branch,
        agent,
        agent_notification_preferences,
        agent_notification_channel_preferences,
        notification_topic,
    """

    # CHECK IF AGENT HAS OPETED IN EMAIL CHANNEL PREFERENCE AND THE AGENT HAS OPTED IN THE NOTIFICATION TOPIC
    if (
        constants.NOTIFICATION_CHANNEL_EMAIL
        in kwargs["agent_notification_channel_preferences"]
        and kwargs["notification_topic"] in kwargs["agent_notification_preferences"]
    ):
        subject = f"Payment Approved order number: {kwargs['payment_order_number']}"

        # GET THE EMAIL CONTENT AND DESTRUCTURE THE RETURNED TUPPLE TO SINGLE VARUABLES
        (
            email_content,
            content_path,
            topic,
        ) = helpers.get_payment_approval_confirmation_email_content(
            kwargs["payment_purpose"]
        )

        # REPLACE THE po_number PLACEHOLDER BY THE ACTUAL PAYMENT ORDER NUMBER
        # email_content = email_content.replace(
        #     "{{po_number}}", kwargs["payment_order_number"]
        # )
        from_email = "grinmove@gmail.com"

        # CALL SEND EMAIL FUNCTION
        send_mail(
            subject,
            "",
            from_email,
            kwargs["recipients"],
            html_message=email_content,
            fail_silently=True,
        )

        gent_branch_instance = get_cached_or_from_db.get_agent_branch(
            kwargs["agent_branch"]
        )

        # CALL create_agent_notification TO CREATE AND SAVE THE NOTIFICATION
        helpers.create_agent_notification(
            title=subject,
            content=content_path,
            notification_topic=topic,
            agent_branch=gent_branch_instance,
            agent=gent_branch_instance.agent,
        )
