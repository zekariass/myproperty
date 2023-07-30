# Generated by Django 4.2 on 2023-07-26 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0002_initial'),
        ('agents', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('opt_in', models.BooleanField(default=True)),
                ('notification_channel', models.CharField(max_length=30)),
                ('notification_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.notificationtopic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255, verbose_name='notification title')),
                ('content', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('notification_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.notificationtopic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentNotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('opt_in', models.BooleanField(default=True)),
                ('notification_channel', models.CharField(max_length=30)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agent')),
                ('notification_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.notificationtopic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255, verbose_name='notification title')),
                ('content', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agents.agent')),
                ('notification_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.notificationtopic')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]