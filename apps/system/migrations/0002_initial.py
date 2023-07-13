# Generated by Django 4.2 on 2023-07-13 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemrating',
            name='user',
            field=models.ForeignKey(blank=True, default=None, help_text='User id will be set to -1 by default if user is anonymous', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='system_ratings', related_query_name='system_rating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='systemparameter',
            name='system',
            field=models.ForeignKey(help_text='The system module that this parameter apply to', on_delete=django.db.models.deletion.CASCADE, related_name='system_parameters', related_query_name='system_parameter', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='systemfeedback',
            name='system',
            field=models.ForeignKey(help_text='The system module that this feedback is given to', on_delete=django.db.models.deletion.CASCADE, related_name='system_feedbacks', related_query_name='system_feedback', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='systemfeedback',
            name='user',
            field=models.ForeignKey(blank=True, default=None, help_text='User id will be set to -1 by default if user is anonymous', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='system_feedbacks', related_query_name='system_feedback', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='systemassetowner',
            name='system',
            field=models.ForeignKey(help_text='The system module that this system asset owner belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='system_asset_owners', related_query_name='system_asset_owner', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='systemasset',
            name='asset_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', related_query_name='asset', to='system.systemassetowner'),
        ),
        migrations.AddField(
            model_name='systemasset',
            name='system',
            field=models.ForeignKey(help_text='The system module that this system asset belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='system_assets', related_query_name='system_asset', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='supportedcardscheme',
            name='system',
            field=models.ForeignKey(help_text='The system module that this supported card scheme applies to', on_delete=django.db.models.deletion.CASCADE, related_name='supported_card_schemes', related_query_name='supported_card_scheme', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='servicesubscriptionplan',
            name='base_currency',
            field=models.ForeignKey(help_text='The default currency for this plan.', on_delete=django.db.models.deletion.CASCADE, related_name='service_subscription_plans', related_query_name='service_subscription_plan', to='system.currency'),
        ),
        migrations.AddField(
            model_name='servicesubscriptionplan',
            name='listing_parameter',
            field=models.ForeignKey(help_text='The discounts are linked to listing parameters so that                                             the system can identify which discount to give to which agent', on_delete=django.db.models.deletion.CASCADE, related_name='service_subscription_plans', related_query_name='service_subscription_plan', to='system.listingparameter'),
        ),
        migrations.AddField(
            model_name='servicesubscriptionplan',
            name='system',
            field=models.ForeignKey(help_text='The system module that this subscription plan applies to', on_delete=django.db.models.deletion.CASCADE, related_name='service_subscription_plans', related_query_name='service_subscription_plan', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='referralrewardplan',
            name='system',
            field=models.ForeignKey(help_text='The system module that this referral reward plan applies to', on_delete=django.db.models.deletion.CASCADE, related_name='referral_reward_plans', related_query_name='referral_reward_plan', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='paymentmethoddiscount',
            name='payment_method',
            field=models.ForeignKey(help_text='The payment method that the discount applies to', on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', related_query_name='payment_method', to='system.paymentmethod', verbose_name='payment method'),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='system',
            field=models.ForeignKey(help_text='The system module that the payment method applies to', on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', related_query_name='payment_method', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='notificationtopic',
            name='system',
            field=models.ForeignKey(help_text='The system module that this feedback is given to', on_delete=django.db.models.deletion.CASCADE, related_name='notification_topics', related_query_name='notification_topic', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='notificationtopic',
            name='target_group',
            field=models.ForeignKey(help_text='The target user group that this notifications to be sent                                         to with is topic', on_delete=django.db.models.deletion.CASCADE, related_name='notification_topics', related_query_name='notification_topic', to='auth.group'),
        ),
        migrations.AddField(
            model_name='listingparameter',
            name='system',
            field=models.ForeignKey(help_text='The system module that this parameter apply to', on_delete=django.db.models.deletion.CASCADE, related_name='listing_parameters', related_query_name='listing_parameter', to='system.system', verbose_name='system module'),
        ),
        migrations.AddField(
            model_name='featuringprice',
            name='base_currency',
            field=models.ForeignKey(help_text='The default currency for this featuring price.', on_delete=django.db.models.deletion.CASCADE, related_name='featuring_prices', related_query_name='featuring_price', to='system.currency'),
        ),
        migrations.AddField(
            model_name='featuringprice',
            name='system',
            field=models.ForeignKey(help_text='The system module that this featuring price applies to', on_delete=django.db.models.deletion.CASCADE, related_name='featuring_prices', related_query_name='featuring_price', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='discount',
            name='listing_parameter',
            field=models.ForeignKey(help_text='The discounts are linked to listing parameters so that                                             the system can identify which discount to give to which agent', on_delete=django.db.models.deletion.CASCADE, related_name='discounts', related_query_name='discount', to='system.listingparameter'),
        ),
        migrations.AddField(
            model_name='currency',
            name='system',
            field=models.ForeignKey(help_text='The system module that the currency applies to', on_delete=django.db.models.deletion.CASCADE, related_name='currencies', related_query_name='currency', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='system',
            field=models.ForeignKey(help_text='The system module that this coupon applies to', on_delete=django.db.models.deletion.CASCADE, related_name='coupons', related_query_name='coupon', to='system.system', verbose_name='System Module'),
        ),
        migrations.AddConstraint(
            model_name='systemrating',
            constraint=models.UniqueConstraint(fields=('user', 'system'), name='user_can_rate_once_constraint', violation_error_message='A user can only rate a system once.                                         Consider editing your rating instead!'),
        ),
        migrations.AddConstraint(
            model_name='systemparameter',
            constraint=models.UniqueConstraint(fields=('system', 'name'), name='system_parameter_unique_together_constraint'),
        ),
        migrations.AddConstraint(
            model_name='systemfeedback',
            constraint=models.UniqueConstraint(fields=('user', 'system'), name='user_can_give_feedback_once_constraint', violation_error_message='A user can give feedback only once.                                         Consider editing your feedback instead!'),
        ),
        migrations.AddConstraint(
            model_name='notificationtopic',
            constraint=models.UniqueConstraint(fields=('system', 'name'), name='notification_topic_unique_together_constraint'),
        ),
        migrations.AddConstraint(
            model_name='listingparameter',
            constraint=models.UniqueConstraint(fields=('system', 'name'), name='listing_parameter_unique_together_constraint'),
        ),
    ]