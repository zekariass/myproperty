import os
import random
import string
import uuid

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.utils import timezone

from . import constants


def generate_unique_code(length):
    code1_len = length // 2
    code2_len = length - code1_len
    characters = string.ascii_uppercase + string.digits
    code1 = "".join(random.choice(characters) for _ in range(code1_len))

    code2 = uuid.uuid4().hex[:code2_len].upper()

    code = code1 + code2

    return code


def generate_agent_branch_code():
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(10))
    return constants.AGENT_BRANCH_CODE_INITIAL + code.upper()


def generate_agent_referral_code():
    characters = string.ascii_uppercase + string.digits
    code = "".join(random.choice(characters) for _ in range(8))
    return constants.AGENT_REFERRAL_CODE_INITIAL + code.upper()


def generate_coupon_code():
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(12))
    return code


def generate_custom_property_id():
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(11))
    return constants.PROPERTY_CUSTOM_ID_INITIAL + code


def create_coupon(coupon, **coupon_data):
    coupon = coupon.objects.create(**coupon_data)
    return coupon


def send_email_to_user(*args, **kwargs):
    send_mail(*args, **kwargs)


def send_referrer_coupon_email(
    referrer_coupon, percentage_value, fixed_value, recipient
):
    subject = "Your Grinmove Coupon!"

    discount_amount = f"{percentage_value}%" if percentage_value else fixed_value

    message = f"""
                <html><body><h1>
                Dear Agent,

                Thank you for referring! You are rewarded for your good job.
                Your coupon code is '{referrer_coupon}'. You can use your coupon when listing your properties.

                Enjoy your {discount_amount} discount.
                
                Earn more coupons by referring to other agents
                </h1></body></html>
                            """
    from_email = "grinmove@gmail.com"
    recipient_list = [recipient]
    send_email_to_user(
        subject,
        "",
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=True,
    )


def send_new_agent_created_email(recipient):
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
    send_email_to_user(
        subject,
        "",
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=True,
    )


def send_referee_coupon_email(referee_coupon, percentage_value, fixed_value, recipient):
    subject = "Your Grinmove Coupon!"

    discount_amount = f"{percentage_value}%" if percentage_value else fixed_value

    message = f"""<html>
                        <style>
                        #congra {{
                            font-weight: "bold"
                            font-size: 2em
                            }}

                        </style>
                        <body>
                            <h5>Dear New Agent,<h5>

                            <p><span id="congra">Congratulations!</span> on your first move with Grinmove! Your agent has been created.
                            Your coupon code is '{referee_coupon}'. You can use your coupon when listing your properties.</p>

                            <p>Enjoy your {discount_amount} discount.</p>

                            <p>Earn more coupons by referring to other agents</p>

                            <a href="http://127.0.0.1:8000/myproperty-api-docmentation/">Check the doc</a>
                        </body></html>"""
    from_email = "grinmove@gmail.com"
    recipient_list = [recipient]
    send_email_to_user(
        subject,
        "",
        from_email,
        recipient_list,
        html_message=message,
        fail_silently=True,
    )


def property_plan_upload_path(instance, filename):
    now = timezone.now()
    _, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"properties/plan/{instance.pk}_{now:%Y:%m:%d:%H:%M:%S}_{milliseconds}{extension}"


def property_image_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename)
    milliseconds = now.microsecond // 1000
    return f"properties/images/{instance.property.pk}_{now:%Y%m%d%H%M%S}_{milliseconds}{extension}"


def property_video_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename)
    milliseconds = now.microsecond // 1000
    return f"properties/videos/{instance.property.pk}_{now:%Y%m%d%H%M%S}_{milliseconds}{extension}"


def bank_receipt_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename)
    milliseconds = now.microsecond // 1000
    return f"payments/bank_receipts/{now:%Y%m%d%H%M%S}_{milliseconds}{extension}"


def mobile_receipt_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename)
    milliseconds = now.microsecond // 1000
    return f"payments/mobile_receipts/{now:%Y%m%d%H%M%S}_{milliseconds}{extension}"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {"errors": response.data}
    # else:
    #     if isinstance(exc, Exception) and int(getattr(exc, "status_code", None)) == 500:
    #         response_data = {"errors": str(exc)}

    #         response = Response(
    #             response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    return response


def generate_payment_order_no():
    characters = string.ascii_uppercase + string.digits
    code = "".join(random.choice(characters) for _ in range(13))
    return constants.PAYMENT_ORDER_INITIAL + code


def get_boolean_url_query_value(request, param):
    if param in request.query_params:
        if request.query_params[param].lower() == "true":
            return True
        elif request.query_params[param].lower() == "false":
            return False
        else:
            return None
