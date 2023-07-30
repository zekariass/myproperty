from rest_framework import serializers

from apps.mixins import constants

from . import models as pay_models


class BankTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.BankTransfer
        fields = "__all__"
        read_only_fields = [
            "transaction_reference_number",
            "paid_on",
            "receipt_path",
            "payment",
        ]


class CardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.CardPayment
        fields = "__all__"


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.VoucherPayment
        fields = "__all__"


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.MobilePayment
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    sub_payment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = pay_models.Payment
        fields = [
            "id",
            "payment_method",
            "order_no",
            "total_amount",
            "currency",
            "exchange_rate",
            "coupon",
            "payment_purpose",
            "is_approved",
            "approved_on",
            "added_on",
            "sub_payment",
        ]
        read_only_fields = [
            "id",
            "order_no",
            "coupon",
            "currency",
            "exchange_rate",
            "is_approved",
            "approved_on",
            "added_on",
        ]

    def get_sub_payment(self, obj):
        if obj.payment_method.name == constants.PAYMENT_METHOD_BANK_TRANSFER:
            sub_payment_instance = pay_models.BankTransfer.objects.get(payment=obj.id)
            return BankTransferSerializer(instance=sub_payment_instance).data
        elif obj.payment_method.name == constants.PAYMENT_METHOD_VOUCHER:
            sub_payment_instance = pay_models.VoucherPayment.objects.get(payment=obj.id)
            return VoucherSerializer(instance=sub_payment_instance).data
        elif obj.payment_method.name == constants.PAYMENT_METHOD_MOBILE_PAYMENT:
            sub_payment_instance = pay_models.MobilePayment.objects.get(payment=obj.id)
            return MobileSerializer(instance=sub_payment_instance).data
        elif obj.payment_method.name == constants.PAYMENT_METHOD_CARD_PAYMENT:
            sub_payment_instance = pay_models.CardPayment.objects.get(payment=obj.id)
            return CardPaymentSerializer(instance=sub_payment_instance).data
