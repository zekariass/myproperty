# Generated by Django 4.2 on 2023-08-12 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_alter_listing_listing_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentunitlisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='condominiumlisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='landlisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='officelisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='othercommercialpropertyunitlisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='rentlisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='salelisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='savedlisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='sharehouselisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='townhouselisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='venuelisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.AlterField(
            model_name='villalisting',
            name='listing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
    ]
