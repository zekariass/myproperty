# Generated by Django 4.2 on 2023-06-26 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_rename_propertykeyfeatures_propertykeyfeature'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='listingpricebypropertycategory',
            name='single_listing_price_by_property_category_constraint',
        ),
        migrations.AlterField(
            model_name='listingpricebypropertycategory',
            name='listing_type',
            field=models.CharField(choices=[('RENT', 'Rent'), ('SALE', 'Sale')], max_length=20),
        ),
        migrations.AlterField(
            model_name='listingpricebypropertycategory',
            name='price_fixed',
            field=models.DecimalField(decimal_places=5, default=0.0, help_text='Fixed value that the agent should pay for listing', max_digits=10),
        ),
        migrations.AlterField(
            model_name='listingpricebypropertycategory',
            name='price_lower_bound',
            field=models.DecimalField(decimal_places=5, default=0.0, help_text='minimum listing price', max_digits=10),
        ),
        migrations.AlterField(
            model_name='listingpricebypropertycategory',
            name='price_percentage',
            field=models.DecimalField(decimal_places=5, default=0.0, help_text='Percentage value of the property price that the agent should pay for listing', max_digits=10),
        ),
        migrations.AlterField(
            model_name='listingpricebypropertycategory',
            name='price_upper_bound',
            field=models.DecimalField(decimal_places=5, default=0.0, help_text='maximum listing price', max_digits=10),
        ),
        migrations.AddConstraint(
            model_name='amenity',
            constraint=models.UniqueConstraint(fields=('id', 'category'), name='unique-amenity-category-constriant'),
        ),
    ]