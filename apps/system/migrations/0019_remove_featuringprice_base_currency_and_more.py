# Generated by Django 4.2 on 2023-08-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0018_alter_listingparameter_name_alter_paymentmethod_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuringprice',
            name='base_currency',
        ),
        migrations.AlterField(
            model_name='notificationtopic',
            name='name',
            field=models.CharField(choices=[('NEW_AGENT_ADDED', 'NEW_AGENT_ADDED'), ('NEW_AGENT_BRANCH_ADDED', 'NEW_AGENT_BRANCH_ADDED'), ('NEW_PROPERTY_ADDED', 'NEW_PROPERTY_ADDED'), ('NEW_LISTING_ADDED', 'NEW_LISTING_ADDED'), ('PAYMENT_ORDER_REQUESTED', 'PAYMENT_ORDER_REQUESTED'), ('PAYMENT_ORDER_APPROVED', 'PAYMENT_ORDER_APPROVED'), ('NEW_AGENT_SERVICE_SUBSCRIPTION', 'NEW_AGENT_SERVICE_SUBSCRIPTION'), ('MARKETING', 'MARKETING'), ('LISTING_VIEWED', 'LISTING_VIEWED'), ('REFERRER_COUPON', 'REFERRER_COUPON'), ('REFEREE_COUPON', 'REFEREE_COUPON')], max_length=200, verbose_name='topic name'),
        ),
        migrations.AlterField(
            model_name='notificationtopic',
            name='target_group',
            field=models.CharField(choices=[('USER', 'USER'), ('AGENT', 'AGENT')], help_text='The target user group that this notifications to be sent                                         to with is topic', max_length=30),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='approval_mode',
            field=models.CharField(choices=[('AUTO', 'AUTO'), ('MANUAL', 'MANUAL')], max_length=30, verbose_name='payment approval mode'),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionplan',
            name='name',
            field=models.CharField(choices=[('AGENT_MONTHLY_BILLED_MONTHLY', 'AGENT_MONTHLY_BILLED_MONTHLY'), ('AGENT_MONTHLY_BILLED_MONTHLY', 'AGENT_MONTHLY_BILLED_MONTHLY'), ('AGENT_MONTHLY_BILLED_SEMI_ANUALLY', 'AGENT_MONTHLY_BILLED_SEMI_ANUALLY'), ('AGENT_MONTHLY_BILLED_YEARLY', 'AGENT_MONTHLY_BILLED_YEARLY')], max_length=200, verbose_name='service subscription plan name'),
        ),
    ]
