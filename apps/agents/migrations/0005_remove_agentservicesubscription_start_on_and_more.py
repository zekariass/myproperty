# Generated by Django 4.2 on 2023-08-04 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_periodicity_and_more'),
        ('agents', '0004_alter_agent_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentservicesubscription',
            name='start_on',
        ),
        migrations.RemoveField(
            model_name='agentservicesubscription',
            name='subscription_amount',
        ),
        migrations.AddField(
            model_name='agentservicesubscription',
            name='subscription_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.servicesubscriptionplan'),
        ),
        migrations.AddField(
            model_name='agentservicesubscription',
            name='subscription_price',
            field=models.DecimalField(decimal_places=2, default=1.0, help_text='it takes its value from subscription_price field of ServiceSubscriptionPlan. This field is to be used as history for future reports', max_digits=10),
            preserve_default=False,
        ),
    ]
