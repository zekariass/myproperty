from rest_framework.response import Response
from rest_framework import status

from apps.payments.serializers import BankTransferSerializer
from apps.mixins import functions, constants


def bank_transfer_interface(request, sub_payment_data, paid_amount, payment):
    try:
        transaction_reference_number = functions.generate_transaction_reference_number(
            constants.PAYMENT_METHOD_BANK_TRANSFER
        )
        bank_transfer_serializer = BankTransferSerializer(data=sub_payment_data)
        bank_transfer_serializer.is_valid(raise_exception=True)
        bank_transfer_serializer.save(
            transaction_reference_number=transaction_reference_number,
            paid_amount=paid_amount,
            payment=payment,
        )
    except Exception as e:
        raise Exception(str(e))

    return True
