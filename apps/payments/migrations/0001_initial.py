# Generated by Django 4.2 on 2023-07-22 20:04

import apps.mixins.functions
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0002_initial'),
        ('agents', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_no', models.CharField(max_length=15, verbose_name='order number')),
                ('transaction_reference_number', models.CharField(max_length=15)),
                ('total_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('exchange_rate', models.DecimalField(decimal_places=5, max_digits=10, max_length=10)),
                ('payment_purpose', models.CharField(blank=True, max_length=250, null=True)),
                ('is_approved', models.BooleanField(default=False, verbose_name='is payment approved')),
                ('ordered_on', models.DateField(default=django.utils.timezone.now)),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.coupon')),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', related_query_name='payment', to='system.currency')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.paymentmethod')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VoucherPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
                ('voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.voucher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_on', models.DateField(default=django.utils.timezone.now)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
                ('service_subscription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='agents.agentservicesubscription')),
            ],
        ),
        migrations.CreateModel(
            name='MobilePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('mobile_app_name', models.CharField(blank=True, max_length=100, null=True)),
                ('paid_on', models.DateField(default=django.utils.timezone.now)),
                ('receipt_path', models.FileField(upload_to=apps.mixins.functions.mobile_receipt_path, verbose_name='receipt')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CardPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('cardholder_name', models.CharField(max_length=100)),
                ('pan', models.CharField(blank=True, max_length=19, null=True)),
                ('pan_token', models.CharField(blank=True, max_length=128, null=True)),
                ('card_issuer', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_gateway', models.CharField(max_length=150)),
                ('paid_on', models.DateField(default=django.utils.timezone.now)),
                ('card_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.supportedcardscheme')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
            ],
        ),
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('bank_name', models.CharField(max_length=150)),
                ('bank_branch_name', models.CharField(max_length=150)),
                ('branch_address', models.CharField(blank=True, max_length=250, null=True)),
                ('paid_on', models.DateField(default=django.utils.timezone.now)),
                ('receipt_path', models.FileField(upload_to=apps.mixins.functions.bank_receipt_path, verbose_name='receipt')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
