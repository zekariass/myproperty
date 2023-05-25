# Generated by Django 4.2 on 2023-05-12 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0008_alter_mypropertyuser_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mypropertyuser',
            name='is_blocked',
        ),
        migrations.AlterField(
            model_name='mypropertyuser',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='users.role', verbose_name='User Roles'),
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='Permissions specific to this user!', related_name='role_set', related_query_name='role', to='auth.permission'),
        ),
    ]
