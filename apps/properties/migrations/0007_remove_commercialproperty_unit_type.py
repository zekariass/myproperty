# Generated by Django 4.2 on 2023-08-12 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_remove_listingpricebypropertycategory_single_listing_price_by_property_category_constraint_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commercialproperty',
            name='unit_type',
        ),
    ]
