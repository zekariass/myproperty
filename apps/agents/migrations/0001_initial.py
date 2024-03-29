# Generated by Django 4.2 on 2023-07-13 16:58

import apps.agents.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=200, verbose_name='agent name')),
                ('motto', models.CharField(blank=True, max_length=100, null=True, verbose_name='agent slogan')),
                ('logo_path', models.ImageField(blank=True, null=True, upload_to=apps.agents.models.create_agent_logo_file_path, verbose_name='company logo')),
                ('referral_code', models.CharField(db_index=True, max_length=15, unique=True, verbose_name='agent referral code')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_superadmin', models.BooleanField(default=False, help_text='Is this user the super administrator of the branch?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('branch_code', models.CharField(db_index=True, max_length=15, unique=True, verbose_name='agent branch code')),
                ('name', models.CharField(max_length=100, verbose_name='agent branch name')),
                ('is_main_branch', models.BooleanField(default=False, verbose_name='is this the main branch of the agent')),
                ('email', models.EmailField(max_length=100, verbose_name='branch email address')),
                ('phone_number', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'Agent branches',
            },
        ),
        migrations.CreateModel(
            name='AgentDiscountTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('used_discounts', models.PositiveIntegerField(default=0, verbose_name='how many discounts used so far?')),
                ('max_discounts', models.PositiveIntegerField(default=0, verbose_name='how many total discounts you have?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentReferral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentReferralReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_referee_reward', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentReferralTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_of_current_referrals', models.PositiveIntegerField(default=1, verbose_name='current number of referrals?')),
                ('is_open', models.BooleanField(default=True, help_text='Does the agent have open/anawarded reward tracker?', verbose_name='is tracker open?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentServiceSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscription_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('request_type', models.CharField(choices=[('VIEW_PROPERTY', 'View the property'), ('AVAILABILITY', 'Check availability'), ('INFORMATION', 'Get more information')], max_length=100, verbose_name='type of request')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('first_name', models.CharField(max_length=50, verbose_name='requester first name')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='requester middle name')),
                ('last_name', models.CharField(max_length=50, verbose_name='requester last name')),
                ('email', models.EmailField(max_length=100, verbose_name='requester email address')),
                ('phone_number', models.CharField(max_length=15, verbose_name='requester phone number')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RequestMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.TextField()),
                ('sender', models.CharField(choices=[('AGENT', 'Agent'), ('CLIENT', 'Client')], max_length=100, verbose_name='message sender')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.request')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
