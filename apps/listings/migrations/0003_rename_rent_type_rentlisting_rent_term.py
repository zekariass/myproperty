# Generated by Django 4.2 on 2023-07-28 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_remove_commercialpropertylisting_commercial_property_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rentlisting',
            old_name='rent_type',
            new_name='rent_term',
        ),
    ]
