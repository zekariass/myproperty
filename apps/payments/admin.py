from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Payment)
admin.site.register(models.VoucherPayment)
admin.site.register(models.BankTransfer)
admin.site.register(models.MobilePayment)
admin.site.register(models.CardPayment)
