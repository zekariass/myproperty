# Generated by Django 4.2 on 2023-08-10 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_alter_listing_listing_type'),
        ('agents', '0006_alter_agentservicesubscription_subscription_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='requests', related_query_name='request', to='listings.listing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='request_type',
            field=models.CharField(choices=[('VIEW_REQUEST', 'VIEW_REQUEST'), ('AVAILABILITY_REQUEST', 'AVAILABILITY_REQUEST'), ('DETAIL_REQUEST', 'DETAIL_REQUEST')], max_length=100, verbose_name='type of request'),
        ),
        migrations.AlterField(
            model_name='requestmessage',
            name='sender',
            field=models.CharField(choices=[('AGENT', 'AGENT'), ('CLIENT', 'CLIENT')], max_length=100, verbose_name='message sender'),
        ),
    ]
