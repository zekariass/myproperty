# Generated by Django 4.2 on 2023-05-26 17:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='country name')),
                ('iso_3166_code', models.CharField(blank=True, max_length=30, null=True, verbose_name='country code')),
                ('latitute', models.CharField(blank=True, max_length=20, null=True, verbose_name='geo latitude')),
                ('longitude', models.CharField(blank=True, max_length=20, null=True, verbose_name='geo logitude')),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('street', models.CharField(max_length=100, verbose_name='street name')),
                ('post_code', models.CharField(blank=True, max_length=10, null=True)),
                ('house_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='house number')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, null=True, verbose_name='geo latitude')),
                ('longitude', models.CharField(blank=True, max_length=20, null=True, verbose_name='geo longitude')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.country')),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
