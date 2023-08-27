from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from celery import shared_task

from apps.notifications.emails.helpers import (
    create_user_notification,
    get_password_changed_confirmation_email_notification_content,
    get_password_reset_link_request_email_notification_content,
)


@shared_task
def send_password_reset_link_email(*args, **kwargs):
    """
    Send password reset email notification to the user

    Keyword arguments:
    - reset_url
    - recipient
    - password_reset_token_lifetime
    """

    # GET USER BY EMAIL
    try:
        user = get_user_model().objects.get(email=kwargs["recipient"])
    except ObjectDoesNotExist:
        raise Exception(f"User with email {kwargs['recipient']} does not exist!")

    # EMAIL SUBJECT
    subject = f"Password reset link!"

    # CONTEXT DATA
    context_data = {
        "reset_url": kwargs["reset_url"],
        "password_reset_token_lifetime": kwargs["password_reset_token_lifetime"],
    }

    # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
    # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
    # BE SAVED INSTEAD OF THE CONTENT ITSELF
    (
        email_content,
        content_path,
        topic,
    ) = get_password_reset_link_request_email_notification_content(
        context_data=context_data
    )

    # SEND THE EMAIL NOTIFICATION
    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [kwargs["recipient"]],
        html_message=email_content,
        fail_silently=True,
    )

    # CREATE AND SAVE THE NOTIFICATION
    create_user_notification(
        title=subject, content=content_path, notification_topic=topic, user=user
    )


@shared_task
def send_password_change_confirmation_email(*args, **kwargs):
    """
    Send password change confirmation email notification to the user

    Keyword arguments:
    - login_url
    - recipient
    """

    # GET USER BY EMAIL
    try:
        user = get_user_model().objects.get(email=kwargs["recipient"])
    except ObjectDoesNotExist:
        raise Exception(f"User with email {kwargs['recipient']} does not exist!")

    # EMAIL SUBJECT
    subject = f"Password changed!"

    # TEMPLATE CONTEXT DATA
    context_data = {"login_url": kwargs["login_url"]}

    # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
    # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
    # BE SAVED INSTEAD OF THE CONTENT ITSELF
    (
        email_content,
        content_path,
        topic,
    ) = get_password_changed_confirmation_email_notification_content(
        context_data=context_data
    )

    # SEND THE EMAIL NOTIFICATION
    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [kwargs["recipient"]],
        html_message=email_content,
        fail_silently=True,
    )

    # CREATE AND SAVE THE NOTIFICATION
    create_user_notification(
        title=subject, content=content_path, notification_topic=topic, user=user
    )
