# Generated by Django 4.2 on 2023-05-11 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_mypropertyuser_options_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
