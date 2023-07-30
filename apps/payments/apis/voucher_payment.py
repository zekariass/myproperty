from django.db.models import F
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status

from apps.payments.models import VoucherPayment
from apps.system.models import Voucher
from apps.mixins import functions, constants


def voucher_payment_interface(request, sub_payment_data, paid_amount, payment):
    # print("================================>: HOHO: ", transfer_data)
    try:
        transaction_reference_number = functions.generate_transaction_reference_number(
            constants.PAYMENT_METHOD_VOUCHER
        )

        try:
            voucher_instance = Voucher.objects.get(id=sub_payment_data["voucher"])
        except ObjectDoesNotExist:
            raise Exception(
                f"Voucher with id {sub_payment_data['voucher']} does not exist."
            )

        if voucher_instance.expire_on <= timezone.now():
            raise Exception(f"Voucher {voucher_instance.code} is outdated.")

        if voucher_instance.current_value < paid_amount:
            raise Exception(f"Voucher {voucher_instance.code} has no enough balance.")

        VoucherPayment.objects.create(
            transaction_reference_number=transaction_reference_number,
            paid_amount=paid_amount,
            payment=payment,
            voucher=voucher_instance,
        )

        Voucher.objects.update(
            id=voucher_instance.id,
            current_value=F("current_value") - paid_amount,
        )
        return True
    except Exception as e:
        raise Exception(str(e))
