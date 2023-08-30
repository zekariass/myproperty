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
        response.data = get_error_response_dict(message=response.data)

    return response


def generate_payment_order_no():
    characters = string.ascii_uppercase + string.digits
    code = "".join(random.choice(characters) for _ in range(13))
    return constants.PAYMENT_ORDER_INITIAL + code


def generate_transaction_reference_number(payment_method):
    characters = string.ascii_letters + string.digits
    code = "".join(random.choice(characters) for _ in range(13))
    return constants.TRANSACTION_REFERENCE_NUMBER_INITIAL[payment_method] + code


def get_boolean_url_query_value(request, param):
    if param in request.query_params:
        if request.query_params[param].lower() == "true":
            return True
        elif request.query_params[param].lower() == "false":
            return False
        else:
            return None


def get_success_response_dict(message=None, data=None):
    return {"message": message, "data": data}


def get_error_response_dict(message="Request was unsuccessful."):
    return {"errors": {"message": message}}
