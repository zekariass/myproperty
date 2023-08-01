from django.core.mail import send_mail

from apps.mixins import constants

from apps.notifications import models as notif_models
from apps.system.models import NotificationTopic


def send_email(*args, **kwargs):
    send_mail(*args, **kwargs)


def send_agent_created_email(recipient):
    subject = "Congratulations! Your Agent is ready to use"
    message = f"""<html>
                        <body>
                            <h5>Dear New Agent,</h5>

                            <p><span style="color=blue; font-weight='bold'">Congratulations!</span> on your first move with Grinmove! Your agent has been created.

                            <p>Earn coupons by referring to other agents</p>

                            <a href="http://127.0.0.1:8000/myproperty-api-docmentation/">Check the doc</a>
                            </body></html>"""
    from_email = "grinmove@gmail.com"
    recipient_list = [recipient]
    send_email(
        subject,
        "",
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=True,
    )


def send_payment_order_recieved_email_to_agent(
    recipients,
    payment_order_number,
    payment_purpose,
    agent_branch_instance,
    agent_notification_preferences,
    agent_notification_channel_preferences,
    current_notification_topic,
):
    """
    This function handles the sending of email notification to agent as the payment order is recieved.
    """

    # CHECK IF AGENT HAS OPETED IN EMAIL CHANNEL PREFERENCE AND THE AGENT HAS OPTED IN THE NOTIFICATION TOPIC
    if (
        constants.NOTIFICATION_CHANNEL_EMAIL in agent_notification_channel_preferences
        and current_notification_topic in agent_notification_preferences
    ):
        subject = "Payment Order"

        # GET THE EMAIL CONTENT AND DESTRUCTURE THE RETURNED TUPPLE TO SINGLE VARUABLES
        (
            email_content,
            content_path,
            topic,
        ) = get_payment_order_confirmation_email_content(payment_purpose)

        # REPLACE THE po_number PLACEHOLDER BY THE ACTUAL PAYMENT ORDER NUMBER
        email_content = email_content.replace("{{po_number}}", payment_order_number)
        from_email = "grinmove@gmail.com"

        # CALL SEND EMAIL FUNCTION
        send_email(
            subject,
            "",
            from_email,
            recipients,
            html_message=email_content,
            fail_silently=True,
        )

        # CALL create_notification TO CREATE AND SAVE THE NOTIFICATION
        create_notification(
            title=subject,
            content=content_path,
            notification_topic=topic,
            agent_branch=agent_branch_instance,
            agent=agent_branch_instance.agent,
        )


def send_payment_approved_email_to_agent(
    recipients,
    payment_order_number,
    payment_purpose,
    agent_branch_instance,
    agent_notification_preferences,
    agent_notification_channel_preferences,
    current_notification_topic,
):
    """
    Send payment approval confirmation email after the payment is approved by admin
    """

    # CHECK IF AGENT HAS OPETED IN EMAIL CHANNEL PREFERENCE AND THE AGENT HAS OPTED IN THE NOTIFICATION TOPIC
    if (
        constants.NOTIFICATION_CHANNEL_EMAIL in agent_notification_channel_preferences
        and current_notification_topic in agent_notification_preferences
    ):
        subject = f"Payment Approved order number: {payment_order_number}"

        # GET THE EMAIL CONTENT AND DESTRUCTURE THE RETURNED TUPPLE TO SINGLE VARUABLES
        (
            email_content,
            content_path,
            topic,
        ) = get_payment_approval_confirmation_email_content(payment_purpose)

        # REPLACE THE po_number PLACEHOLDER BY THE ACTUAL PAYMENT ORDER NUMBER
        email_content = email_content.replace("{{po_number}}", payment_order_number)
        from_email = "grinmove@gmail.com"

        # CALL SEND EMAIL FUNCTION
        send_email(
            subject,
            "",
            from_email,
            recipients,
            html_message=email_content,
            fail_silently=True,
        )

        # CALL create_notification TO CREATE AND SAVE THE NOTIFICATION
        create_notification(
            title=subject,
            content=content_path,
            notification_topic=topic,
            agent_branch=agent_branch_instance,
            agent=agent_branch_instance.agent,
        )


def get_payment_order_confirmation_email_content(payment_purpose):
    """
    Get the right content for the specific payment order notification.
    the notification depends on the payment purpose.
    """

    # ACTUAL EMAIL CONTENT TO BE READ FROM FILE
    email_content = None

    # THE CONTENT FILE PATH TO BE SAVED IN DB
    content_path = None

    # TOPIC OF THE EMAIL NOTIFICATION TO BE READ FROM CONSTANTS MODULE
    topic = None
    if payment_purpose == constants.PAYMENT_PURPOSE_FEATURING:
        topic = get_notification_topic(
            constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED
        )
        content_path = "apps/notifications/notif_templates/email_templates/featuring_payment_requested.html"
        with open(content_path) as file:
            email_content = file.read()
    elif payment_purpose == constants.PAYMENT_PURPOSE_LISTING:
        topic = get_notification_topic(
            constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED
        )
        content_path = "apps/notifications/notif_templates/email_templates/listing_payment_requested.html"
        with open(content_path) as file:
            email_content = file.read()
    elif payment_purpose == constants.PAYMENT_PURPOSE_SUBSCRIPTION:
        topic = get_notification_topic(
            constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED
        )
        content_path = "apps/notifications/notif_templates/email_templates/new_service_subscription.html"
        with open(content_path) as file:
            email_content = file.read()
    else:
        email_content = ""
    return (email_content, content_path, topic)


def get_payment_approval_confirmation_email_content(payment_purpose):
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
    if payment_purpose == constants.PAYMENT_PURPOSE_FEATURING:
        topic = get_notification_topic(
            constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED
        )
        content_path = "apps/notifications/notif_templates/email_templates/featuring_payment_approved.html"
        with open(content_path) as file:
            email_content = file.read()
    elif payment_purpose == constants.PAYMENT_PURPOSE_LISTING:
        topic = get_notification_topic(
            constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED
        )
        content_path = "apps/notifications/notif_templates/email_templates/listing_payment_approved.html"
        with open(content_path) as file:
            email_content = file.read()
    elif payment_purpose == constants.PAYMENT_PURPOSE_SUBSCRIPTION:
        topic = get_notification_topic(
            constants.NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED
        )
        content_path = "apps/notifications/notif_templates/email_templates/new_service_subscription.html"
        with open(content_path) as file:
            email_content = file.read()
    else:
        email_content = ""
    return (email_content, content_path, topic)


def get_notification_topic(topic_name):
    # Get notification topic from the database
    try:
        topic = NotificationTopic.objects.get(name=topic_name)
    except Exception as e:
        raise Exception(f"File: {__file__}, function: get_notification_topic: {str(e)}")
    return topic


def create_notification(**kwargs):
    # Create the notifiocation and save to DB
    try:
        notif_models.AgentNotification.objects.create(**kwargs)
    except Exception as e:
        raise Exception(f"File: {__file__} function: create_notification: {str(e)}")
