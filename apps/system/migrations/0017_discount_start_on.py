# Generated by Django 4.2 on 2023-08-08 21:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_discount_expire_on_alter_discount_action_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='start_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
