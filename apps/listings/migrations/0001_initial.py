# Generated by Django 4.2 on 2023-07-26 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agents', '0002_initial'),
        ('payments', '0002_payment_approved_on'),
        ('system', '0002_initial'),
        ('properties', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.apartment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialPropertyListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('commercial_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.commercialproperty')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing_type', models.CharField(choices=[('RENT', 'Rent'), ('SALE', 'Sale')], max_length=30)),
                ('listing_payment_type', models.CharField(choices=[('SUBSCRIPTION', 'Subscription'), ('PAY_PER_LISTING', 'Pay per listing')], max_length=30)),
                ('property_price', models.DecimalField(decimal_places=5, default=0.0, max_digits=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('featured_on', models.DateTimeField(blank=True, null=True)),
                ('agent_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agentbranch')),
                ('featuring_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_listings', to='payments.payment')),
                ('listing_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='payments.payment')),
                ('main_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
                ('property_price_currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VillaListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('villa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.villa')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VenueListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.venue')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TownhouseListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('townhouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.townhouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SharehouseListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('sharehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.sharehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SavedListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.room')),
                ('sharehouse_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.sharehouselisting')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RentListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('rent_payment_period', models.CharField(choices=[('DAY', 'Day'), ('WEEK', 'Week'), ('MONTH', 'Month'), ('YEAR', 'Year')], max_length=20)),
                ('rent_type', models.CharField(choices=[('LONG_TERM', 'Long term'), ('SHORT_TERM', 'Short term')], max_length=20)),
                ('deposit_amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=20)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherCommercialPropertyUnitListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('commercial_property_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.commercialpropertylisting')),
                ('other_commercial_property_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.othercommercialpropertyunit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfficeListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('commercial_property_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.commercialpropertylisting')),
                ('office_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.officeunit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LandListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('land', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.land')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CondominiumListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.condominium')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='commercialpropertylisting',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
        migrations.CreateModel(
            name='ApartmentUnitListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('apartment_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.apartmentlisting')),
                ('apartment_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.apartmentunit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='apartmentlisting',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing'),
        ),
    ]