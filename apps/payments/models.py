from django.db import models
from django.utils import timezone

from apps.system import models as sys_models
from apps.agents.models import AgentServiceSubscription
from apps.mixins.common_fields import AddedOnFieldMixin
from apps.mixins.functions import mobile_receipt_path, bank_receipt_path


class Payment(AddedOnFieldMixin):
    order_no = models.CharField("order number", max_length=15)
    payment_method = models.ForeignKey(
        sys_models.PaymentMethod, on_delete=models.SET_NULL, null=True
    )
    total_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    currency = models.ForeignKey(
        sys_models.Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name="payments",
        related_query_name="payment",
    )
    # payment_currency = models.ForeignKey(
    #     sys_models.Currency, on_delete=models.SET_NULL, null=True,
    # )
    exchange_rate = models.DecimalField(
        max_digits=10, decimal_places=5, max_length=10, default=1.00000
    )
    coupon = models.ForeignKey(sys_models.Coupon, on_delete=models.SET_NULL, null=True)
    payment_purpose = models.CharField(max_length=250, null=True, blank=True)
    is_approved = models.BooleanField(
        "is payment approved",
        default=False,
    )
    approved_on = models.DateField(
        null=True,
    )
    # ordered_on = models.DateField(
    #     default=timezone.now,
    # )

    def __str__(self) -> str:
        return f"{self.id}, {self.order_no}, £{self.total_amount}"


class VoucherPayment(AddedOnFieldMixin):
    transaction_reference_number = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    voucher = models.ForeignKey(
        sys_models.Voucher, on_delete=models.SET_NULL, null=True
    )
    paid_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)

    def __str__(self) -> str:
        return f"Voucher: {self.voucher}, {self.paid_amount}"


class BankTransfer(AddedOnFieldMixin):
    transaction_reference_number = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    bank_name = models.CharField(max_length=150)
    bank_branch_name = models.CharField(max_length=150)
    branch_address = models.CharField(max_length=250, blank=True, null=True)
    paid_on = models.DateField(
        default=timezone.now,
    )
    receipt_path = models.FileField("receipt", upload_to=bank_receipt_path)

    def __str__(self) -> str:
        return f"Bank Transfer: {self.bank_name}, {self.paid_amount}"


class MobilePayment(AddedOnFieldMixin):
    transaction_reference_number = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    service_provider = models.CharField(max_length=100, blank=True, null=True)
    paid_on = models.DateField(
        default=timezone.now,
    )
    receipt_path = models.FileField("receipt", upload_to=mobile_receipt_path)

    def __str__(self) -> str:
        return f"Mobile Payment: {self.service_provider if self.service_provider else ' '}, {self.paid_amount}"


class CardPayment(models.Model):
    transaction_reference_number = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=5, default=0.00000)
    cardholder_name = models.CharField(max_length=100)
    pan = models.CharField(max_length=19, null=True, blank=True)
    pan_token = models.CharField(max_length=128, null=True, blank=True)
    card_issuer = models.CharField(max_length=100, null=True, blank=True)
    payment_gateway = models.CharField(max_length=150)
    card_type = models.ForeignKey(
        sys_models.SupportedCardScheme, on_delete=models.SET_NULL, null=True
    )
    paid_on = models.DateField(
        default=timezone.now,
    )

    def __str__(self) -> str:
        return f"Card Payment: {self.card_type.name}, {self.paid_amount}"
