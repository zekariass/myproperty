# Generated by Django 4.2 on 2023-07-13 16:58

import apps.mixins.common_fields
import apps.mixins.functions
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commons', '0001_initial'),
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='amenity name')),
            ],
        ),
        migrations.CreateModel(
            name='AmenityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='amenity category name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=30, verbose_name='property status')),
                ('floors', models.PositiveIntegerField(default=0, verbose_name='number of floors in the building')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApartmentUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bed rooms')),
                ('bath_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bath rooms')),
                ('floor', models.IntegerField(default=0, verbose_name='floor/storey level')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='housing area')),
                ('is_furnished', models.BooleanField(default=False)),
                ('unit_name_or_number', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApartmentUnitAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('APARTMENT', 'Apartment'), ('CONDOMINIUM', 'Condominium'), ('TOWNHOUSE', 'Townhouse'), ('VILLA', 'Villa'), ('OTHER', 'Other')], max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommercialProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('has_parking_space', models.BooleanField(default=False, verbose_name='is the commercial property new?')),
                ('floors', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('NEW', 'New'), ('RESTORED', 'Restored'), ('IN_GOOD_CONDITION', 'In Good Condition'), ('OLD', 'OLD')], max_length=50, verbose_name='current status of the property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bed rooms')),
                ('bath_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bath rooms')),
                ('floor', models.IntegerField(default=0, verbose_name='floor/storey level')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='housing area')),
                ('is_furnished', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('RESTORED', 'Restored'), ('IN_GOOD_CONDITION', 'In Good Condition'), ('OLD', 'OLD')], max_length=50, verbose_name='current status of the property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('area', models.FloatField(default=0.0, verbose_name='area of the land')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='LandType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='land type name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListingPriceByPropertyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing_type', models.CharField(choices=[('RENT', 'Rent'), ('SALE', 'Sale')], max_length=20)),
                ('price_percentage', models.DecimalField(decimal_places=5, default=0.0, help_text='Percentage value of the property price that the agent should pay for listing', max_digits=10)),
                ('price_fixed', models.DecimalField(decimal_places=5, default=0.0, help_text='Fixed value that the agent should pay for listing', max_digits=10)),
                ('price_lower_bound', models.DecimalField(decimal_places=5, default=0.0, help_text='minimum listing price', max_digits=10)),
                ('price_upper_bound', models.DecimalField(decimal_places=5, default=0.0, help_text='maximum listing price', max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ListingPriceByPropertyCategoryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('listing_type', models.CharField(max_length=20)),
                ('price_percentage', models.DecimalField(decimal_places=5, help_text='Percentage value of the property price that the agent should pay for listing', max_digits=10)),
                ('price_fixed', models.DecimalField(decimal_places=5, help_text='Fixed value that the agent should pay for listing', max_digits=10)),
                ('price_lower_bound', models.DecimalField(decimal_places=5, help_text='minimum listing price', max_digits=10)),
                ('price_upper_bound', models.DecimalField(decimal_places=5, help_text='maximum listing price', max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OfficeUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('floor', models.IntegerField(default=0, verbose_name='floor/storey level')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='housing area')),
                ('is_furnished', models.BooleanField(default=False)),
                ('unit_name_or_number', models.CharField(max_length=100)),
                ('seats', models.PositiveIntegerField(default=1, verbose_name='number of seats the office is enough for?')),
                ('rooms', models.PositiveIntegerField(default=1, verbose_name='number of rooms in the office?')),
                ('commercial_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office_units', related_query_name='office_unit', to='properties.commercialproperty', verbose_name='parent commercial property')),
            ],
        ),
        migrations.CreateModel(
            name='OtherCommercialPropertyUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('floor', models.IntegerField(default=0, verbose_name='floor/storey level')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='housing area')),
                ('unit_name_or_number', models.CharField(max_length=100)),
                ('rooms', models.PositiveIntegerField(default=1, verbose_name='number of rooms in the unit?')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('custom_prop_id', models.CharField(max_length=15, unique=True, verbose_name='custom property id')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Prperty name or label')),
                ('is_residential', models.BooleanField(default=True, verbose_name='is property for residence?')),
                ('tenure', models.CharField(choices=[('FREEHOLD', 'Freehold'), ('LEASEHOLD', 'Leasehold'), ('COMMONHOLD', 'Commonhold')], max_length=100)),
                ('tax_band', models.CharField(choices=[('BAND_A', 'Band A'), ('BAND_B', 'Band B'), ('BAND_C', 'Band C')], max_length=50)),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address_properties', related_query_name='address_property', to='commons.address', verbose_name='property address')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_properties', related_query_name='agent_property', to='agents.agent', verbose_name='property agent')),
                ('agent_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_properties', related_query_name='branch_property', to='agents.agentbranch', verbose_name='property agent branch')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='property category name')),
                ('cat_key', models.CharField(choices=[('PROPCAT001', 'Apartment'), ('PROPCAT002', 'Condominium'), ('PROPCAT003', 'Townhouse'), ('PROPCAT004', 'Villa'), ('PROPCAT005', 'Sharehouse'), ('PROPCAT006', 'Commercial Property'), ('PROPCAT007', 'Venue'), ('PROPCAT008', 'Land')], max_length=10, unique=True, verbose_name='property category key')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyImageLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='image label name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Villa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bed rooms')),
                ('bath_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bath rooms')),
                ('is_furnished', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('RESTORED', 'Restored'), ('IN_GOOD_CONDITION', 'In Good Condition'), ('OLD', 'OLD')], max_length=50, verbose_name='current status of the property')),
                ('total_compound_area', models.FloatField(default=0.0)),
                ('housing_area', models.FloatField(default=0.0)),
                ('floors', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of fields')),
                ('parent_property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='villa', to='properties.property', verbose_name='main property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('seat_capacity', models.PositiveIntegerField(default=5, verbose_name='how many seats the venue has?')),
                ('total_capacity', models.PositiveIntegerField(default=5, verbose_name='total capacity including standing')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='venue area')),
                ('parent_property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='venue', to='properties.property', verbose_name='main property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='Townhouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bed rooms')),
                ('bath_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bath rooms')),
                ('floor', models.IntegerField(default=0, verbose_name='floor/storey level')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='housing area')),
                ('is_furnished', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('RESTORED', 'Restored'), ('IN_GOOD_CONDITION', 'In Good Condition'), ('OLD', 'OLD')], max_length=50, verbose_name='current status of the property')),
                ('structure', models.CharField(choices=[('DETACHED', 'Detached'), ('SEMI_DETACHED', 'Semi Detached'), ('TERRACED', 'Terraced'), ('IN_COMPOUND', 'In Compound')], max_length=100, verbose_name='property structure')),
                ('parent_property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='townhouse', to='properties.property', verbose_name='main property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='Sharehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('floor', models.IntegerField(default=0, verbose_name='Home floor level')),
                ('total_area', models.FloatField(default=0.0)),
                ('shared_rooms_furnished', models.BooleanField(default=False, verbose_name='is the home furnished?')),
                ('status', models.CharField(choices=[('NEW', 'New'), ('RESTORED', 'Restored'), ('IN_GOOD_CONDITION', 'In Good Condition'), ('OLD', 'OLD')], max_length=50, verbose_name='current status of the property')),
                ('structure', models.CharField(choices=[('DETACHED', 'Detached'), ('SEMI_DETACHED', 'Semi Detached'), ('TERRACED', 'Terraced'), ('IN_COMPOUND', 'In Compound')], max_length=100, verbose_name='property structure')),
                ('building_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='building_types', related_query_name='building_type', to='properties.buildingtype', verbose_name='building type')),
                ('parent_property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sharehouse', to='properties.property', verbose_name='main property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('bed_rooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='number of bed rooms')),
                ('floor', models.IntegerField(default=0, verbose_name='floor/storey level')),
                ('area', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='housing area')),
                ('is_furnished', models.BooleanField(default=False)),
                ('has_ensuite_bathroom', models.BooleanField(default=False, verbose_name='does the room has ensuite bathroom?')),
                ('for_gender', models.CharField(choices=[('MALE', 'Male'), ('Female', 'Female'), ('ANY', 'Any')], max_length=30, verbose_name='required of gender of new flatmate')),
                ('for_speaker_of_languages', models.CharField(blank=True, max_length=100, null=True, verbose_name='speaker of language needed')),
                ('flatmate_interests', models.CharField(blank=True, max_length=200, null=True, verbose_name='what interests new flatmate expected to have?')),
                ('occupied', models.BooleanField(default=False, verbose_name='is the room occupied?')),
                ('sharehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', related_query_name='room', to='properties.sharehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_path', models.FileField(upload_to=apps.mixins.functions.property_video_path, verbose_name='property video')),
                ('file_ext', models.CharField(blank=True, max_length=10, null=True, verbose_name='file extension')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_videos', related_query_name='property_video', to='properties.property')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('label', models.CharField(blank=True, max_length=100, null=True, verbose_name='plan label')),
                ('file_path', models.ImageField(upload_to=apps.mixins.functions.property_plan_upload_path, verbose_name='plan label')),
                ('file_ext', models.CharField(blank=True, max_length=10, null=True, verbose_name='file extension')),
                ('parent_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_plans', related_query_name='property_plan', to='properties.property')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, apps.mixins.common_fields.CommonPropertyShallowFieldsMixin),
        ),
        migrations.CreateModel(
            name='PropertyKeyFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=150, verbose_name='feature name')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_features', related_query_name='key_feature', to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_path', models.ImageField(upload_to=apps.mixins.functions.property_image_path, verbose_name='property image')),
                ('file_ext', models.CharField(blank=True, max_length=10, null=True, verbose_name='file extension')),
                ('label', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='label_images', related_query_name='label_image', to='properties.propertyimagelabel')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_images', related_query_name='property_image', to='properties.property')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyCategoryAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.amenity')),
                ('property_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.propertycategory')),
            ],
        ),
        migrations.AddField(
            model_name='propertycategory',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='property_categories', related_query_name='property_category', through='properties.PropertyCategoryAmenity', to='properties.amenity'),
        ),
        migrations.CreateModel(
            name='PropertyAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.amenity')),
                ('parent_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='amenity',
            field=models.ManyToManyField(blank=True, related_name='amenity_properties', related_query_name='amenity_property', through='properties.PropertyAmenity', to='properties.amenity'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_properties', to='properties.propertycategory'),
        ),
        migrations.CreateModel(
            name='OtherCommercialPropertyUnitAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.amenity')),
                ('other_commercial_property_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.othercommercialpropertyunit')),
            ],
        ),
        migrations.AddField(
            model_name='othercommercialpropertyunit',
            name='amenities',
            field=models.ManyToManyField(through='properties.OtherCommercialPropertyUnitAmenity', to='properties.amenity'),
        ),
        migrations.AddField(
            model_name='othercommercialpropertyunit',
            name='commercial_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_units', related_query_name='other_unit', to='properties.commercialproperty', verbose_name='parent commercial property'),
        ),
        migrations.AddField(
            model_name='othercommercialpropertyunit',
            name='property_plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='properties.propertyplan'),
        ),
        migrations.CreateModel(
            name='OfficeUnitAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.amenity')),
                ('office_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.officeunit')),
            ],
        ),
        migrations.AddField(
            model_name='officeunit',
            name='property_plan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='properties.propertyplan'),
        ),
    ]
