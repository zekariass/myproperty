from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

from apps.agents import get_cached_or_from_db
from apps.notifications.emails.helpers import (
    create_notification,
    get_new_listing_added_notification_content,
)


@shared_task
def send_new_listing_added_email_to_agent(*args, **kwargs):
    agent_branch_instance = get_cached_or_from_db.get_agent_branch(
        kwargs["agent_branch"]
    )

    # EMAIL SUBJECT
    subject = f"New listing added"

    # CONTEXT DATA TO BE SENT THE TEMPLATE
    context_data = {
        "property_category_name": kwargs["property_category_name"],
        "property_address": kwargs["property_address"],
        "listing_id": kwargs["listing_id"],
    }

    # GET EMAIL CONTENT, CONTENT PATH AND THE TOPIC OF THE NOTIFICATION
    # THE NOTIFICATION WILL BE SAVED TO DB BUT THE PATH OF THE TEMPLATE WILL
    # BE SAVED INSTEAD OF THE CONTENT ITSELF
    (
        email_content,
        content_path,
        topic,
    ) = get_new_listing_added_notification_content(context_data)

    # SEND THE EMAIL
    send_mail(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [agent_branch_instance.email],
        html_message=email_content,
        fail_silently=True,
    )

    # CREATE THE NOTIFICATION AND SAVE TO DB
    create_notification(
        title=subject,
        content=content_path,
        notification_topic=topic,
        agent_branch=agent_branch_instance,
        agent=agent_branch_instance.agent,
    )
