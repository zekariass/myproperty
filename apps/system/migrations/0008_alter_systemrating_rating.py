# Generated by Django 4.2 on 2023-05-20 13:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_servicesubscriptionplan_base_number_of_branchs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemrating',
            name='rating',
            field=models.PositiveIntegerField(default=5, help_text='Rating value out of 5', validators=[django.core.validators.MaxValueValidator(5, 'Rating must not be greater than 5')], verbose_name='System rating value'),
        ),
    ]
