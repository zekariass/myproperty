# Generated by Django 4.2 on 2023-08-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_alter_savedlisting_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentlisting',
            name='rent_term',
            field=models.CharField(choices=[('LONG_TERM', 'LONG_TERM'), ('LONG_TERM', 'LONG_TERM')], max_length=20),
        ),
    ]
