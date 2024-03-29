# Generated by Django 4.2 on 2023-07-31 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_remove_notificationtopic_notification_topic_unique_together_constraint_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='featuringprice',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='listingparameter',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='notificationtopic',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='notificationtopic',
            name='name',
            field=models.CharField(choices=[('NEW_PROPERTY_ADDED', 'New Property Addded'), ('NEW_LISTING_ADDED', 'New Listing Addded'), ('LISTING_PAYMENT_ORDER_REQUESTED', 'Listing Payment Order Requested'), ('LISTING_PAYMENT_OREDR_APPROVED', 'Listing Payment Order Approved'), ('FEATURING_PAYMENT_ORDER_REQUESTED', 'Featuring Payment Order Requested'), ('FEATURING_PAYMENT_OREDR_APPROVED', 'Featuring Payment Order Approved'), ('SUBSCRIPTION_PAYMENT_OREDR_APPROVED', 'Subscription Payment Order Approved'), ('SUBSCRIPTION_PAYMENT_ORDER_REQUESTED', 'Subscription Payment Order Requested'), ('MARKETING', 'Marketing'), ('LISTING_VIEWED', 'Listing Viewed')], max_length=200, verbose_name='topic name'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='paymentmethoddiscount',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='referralrewardplan',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='servicesubscriptionplan',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='supportedcardscheme',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='system',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='systemasset',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='systemassetowner',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='systemparameter',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
