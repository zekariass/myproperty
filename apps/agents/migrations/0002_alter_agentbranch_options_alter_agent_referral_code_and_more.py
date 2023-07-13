# Generated by Django 4.2 on 2023-06-02 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agentbranch',
            options={'verbose_name_plural': 'Agent branches'},
        ),
        migrations.AlterField(
            model_name='agent',
            name='referral_code',
            field=models.CharField(db_index=True, max_length=15, unique=True, verbose_name='agent referral code'),
        ),
        migrations.AlterField(
            model_name='agentbranch',
            name='branch_code',
            field=models.CharField(db_index=True, max_length=15, unique=True, verbose_name='agent branch code'),
        ),
    ]