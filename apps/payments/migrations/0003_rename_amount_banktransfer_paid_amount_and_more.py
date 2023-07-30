# Generated by Django 4.2 on 2023-07-29 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_approved_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banktransfer',
            old_name='amount',
            new_name='paid_amount',
        ),
        migrations.RenameField(
            model_name='cardpayment',
            old_name='amount',
            new_name='paid_amount',
        ),
        migrations.RenameField(
            model_name='mobilepayment',
            old_name='amount',
            new_name='paid_amount',
        ),
        migrations.RenameField(
            model_name='mobilepayment',
            old_name='mobile_app_name',
            new_name='service_provider',
        ),
        migrations.RenameField(
            model_name='voucherpayment',
            old_name='amount',
            new_name='paid_amount',
        ),
        migrations.DeleteModel(
            name='SubscriptionPayment',
        ),
    ]
