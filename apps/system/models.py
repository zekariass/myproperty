import os

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Group
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator

from apps.mixins.common_fields import (DescriptionAndAddedOnFieldMixin,
                                      AddedOnFieldMixin,
                                      ExpireOnFieldMixin,
                                      StartAndExpireOnFieldMixin)
from apps.mixins import constants

class System(DescriptionAndAddedOnFieldMixin):
    name = models.CharField("system module name", 
                            max_length=100, 
                            unique=True, 
                            choices=constants.SYSTEM_MODULE_NAMES)


    def __str__(self):
        return f"{self.name}"


"""
There are different computations the system perform during processing a functionality, such as listing
"""
class ListingParameter(DescriptionAndAddedOnFieldMixin):

    system = models.ForeignKey(System, 
                               verbose_name="system module", 
                               on_delete=models.CASCADE, 
                               help_text="The system module that this parameter apply to",
                               related_name="listing_parameters",
                               related_query_name="listing_parameter")
    name = models.CharField("parameter name", max_length=200, unique=True, choices=constants.LISTING_PARAMETER_NAMES)
    value = models.CharField("parameter value", max_length=100, blank=True, default="", 
                             help_text="It is any value associated with the listing parameter. \
                                        The value could be integer, string or boolean. \
                                        Value type cast will be done when actually using the value")
    will_expire_after_days = models.PositiveIntegerField("How many days will conf stay valid", default=1)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("system", "name"), name="listing_parameter_unique_together_constraint")
        ]

    def __str__(self):
        return f"{self.name}, {self.system}"




"""
System parameter is a general parameter that is used for different system level configuration. 
It allows to dynamically change different system level values or data.
"""
class SystemParameter(DescriptionAndAddedOnFieldMixin):

    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this parameter apply to",
                               related_name="system_parameters",
                               related_query_name="system_parameter")
    name = models.CharField("parameter name", max_length=200, unique=True)
    value = models.CharField("parameter value", max_length=100, blank=True, default="", 
                             help_text="is any value attached to the parameter. For example, \
                             16 listing per page")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("system", "name"), name="system_parameter_unique_together_constraint")
        ]

    def __str__(self):
        return f"{self.name}, {self.system}"




class Currency(AddedOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that the currency applies to",
                                related_name="currencies",
                               related_query_name="currency")
    name = models.CharField("currency name", max_length=50, unique=True)
    iso_4217_alpha_code = models.CharField("alphabetic code of the currency", max_length=3, unique=True, default="ETB")
    iso_4217_num_code = models.CharField("numeric code of the currency", max_length=3, unique=True, default="230")
    is_default = models.BooleanField(default=False)
    exchange_rate = models.DecimalField(decimal_places=5, max_digits=10, default=0.000, blank=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.name}"
    


class PaymentMethod(DescriptionAndAddedOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that the payment method applies to",
                               related_name="payment_methods",
                               related_query_name="payment_method")
    name = models.CharField("payment method name", max_length=100, unique=True)
    
    
    def __str__(self):
        return f"{self.name}"
    


class PaymentMethodDiscount(StartAndExpireOnFieldMixin,
                            DescriptionAndAddedOnFieldMixin):
    payment_method = models.ForeignKey(PaymentMethod, 
                                       verbose_name="payment method", 
                                       on_delete=models.CASCADE, 
                                       help_text="The payment method that the discount applies to",
                                       related_name="payment_methods",
                                       related_query_name="payment_method")
    discount_percentage_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    discount_fixed_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)

    def __str__(self):
        return f"{self.payment_method}: {self.discount_percentage_value}% | {self.discount_percentage_value}"
   
    

class Discount(AddedOnFieldMixin,
               DescriptionAndAddedOnFieldMixin):
    
    
    name = models.CharField("discount name", max_length=200, unique=True)
    listing_parameter = models.ForeignKey(ListingParameter, 
                                          on_delete=models.CASCADE,
                                          related_name="discounts",
                                          related_query_name="discount",
                                          help_text="The discounts are linked to listing parameters so that \
                                            the system can identify which discount to give to which agent")
    action = models.CharField(verbose_name = "Discount Action Type",
                              max_length=50, 
                              choices=constants.DISCOUNT_ACTIONS,
                              help_text="determines how the system calculated length of discount period \
                                or amount. It can have count, single, or deadline.")
    unit = models.CharField("discount value unit",
                            choices=constants.DISCOUNT_UNITS,
                            max_length=50,
                            help_text="It can be days, listings or subscription"
                            )
    value = models.IntegerField(default=1, help_text="Unit value. i.e. 5 days, or 10 listings, etc", blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    discount_percentage_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    discount_fixed_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    discount_type = models.CharField(choices=constants.DISCOUNT_TYPES, max_length=50)
    is_active = models.BooleanField(default=True)
    is_trackable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"



class ServiceSubscriptionPlan(DescriptionAndAddedOnFieldMixin):
    name = models.CharField("service subscription plan name", max_length=200)
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this subscription plan applies to",
                               related_name="service_subscription_plans",
                               related_query_name="service_subscription_plan")
    listing_parameter = models.ForeignKey(ListingParameter, 
                                          on_delete=models.CASCADE,
                                          related_name="service_subscription_plans",
                                          related_query_name="service_subscription_plan",
                                          help_text="The discounts are linked to listing parameters so that \
                                            the system can identify which discount to give to which agent")
    base_price = models.DecimalField("base subscription plan", decimal_places=5,  max_digits=12)
    period_unit = models.CharField("unit of period",max_length=20, choices=constants.PERIODS)
    period_length = models.PositiveIntegerField("length of period", default=1)
    base_currency = models.ForeignKey(Currency, 
                                      on_delete=models.CASCADE,
                                      related_name="service_subscription_plans",
                                      related_query_name="service_subscription_plan",
                                      help_text="The default currency for this plan.")
    billing_cycle = models.CharField("unit of billing period", max_length=20, choices=constants.PERIODS)
    billing_cycle_length = models.PositiveIntegerField("length of billing period", default=1)
    base_number_of_branchs = models.PositiveIntegerField("Base number of branchs", 
                                                         default=1,
                                                         help_text= "Maximum number of branchs with the base price. \
                                                                    If more than this number, then addtional fees apply.")
    price_increase_by_branch_percentage = models.DecimalField(decimal_places=2,  
                                                              max_digits=12,
                                                              default=0.00, 
                                                              help_text="The percentage of the base price \
                                                                that the subscription plan price is increased \
                                                                  as the number of branches encrease")
    price_increase_by_branch_fixed = models.DecimalField(decimal_places=2,  
                                                         max_digits=12, 
                                                         default=0.00,
                                                         help_text="The fixed rate that the subscription plan \
                                                         price is increased as the number of branches encrease")
    

    def __str__(self):
        return f"{self.name}"
    
    
class SystemRating(AddedOnFieldMixin):
    """Users can give ratings of their user experience about the system by number rating"""
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this rating is given to",
                               related_name="system_ratings",
                               related_query_name="system_rating")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_DEFAULT, 
                             related_name="system_ratings",
                             related_query_name="system_rating",
                             null=True, 
                             blank=True,
                             default = None,
                             help_text="User id will be set to -1 by default if user is anonymous")
    rating = models.PositiveIntegerField("System rating value", 
                                         default=5,
                                         validators=[MaxValueValidator(5, message="Rating must not be greater than 5")],
                                         help_text="Rating value out of 5")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "system"], 
                                    name="user_can_rate_once_constraint",
                                    violation_error_message="A user can only rate a system once. \
                                        Consider editing your rating instead!")
        ]

    def __str__(self):
        return f"{self.system}: {self.rating}"

class SystemFeedback(AddedOnFieldMixin):
    """Users can write any feedback about the system. Feedback is a comment about their user experience of the system. 
    It allows to improve the system with additional features or modify the existing one"""
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this feedback is given to",
                               related_name="system_feedbacks",
                               related_query_name="system_feedback")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_DEFAULT, 
                             related_name="system_feedbacks",
                             related_query_name="system_feedback",
                             null=True, 
                             blank=True,
                             default = None,
                             help_text="User id will be set to -1 by default if user is anonymous")
    feedback = models.TextField("System feedback")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "system"], 
                                    name="user_can_give_feedback_once_constraint",
                                    violation_error_message="A user can give feedback only once. \
                                        Consider editing your feedback instead!")
        ]

    def __str__(self):
        return f"{self.feedback}"[:30]+"..."

class NotificationTopic(DescriptionAndAddedOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this feedback is given to",
                               related_name="notification_topics",
                               related_query_name="notification_topic")
    name = models.CharField("topic name", max_length=200)
    target_group = models.ForeignKey(Group, 
                                     on_delete=models.CASCADE, 
                                     related_name="notification_topics",
                                     related_query_name="notification_topic",
                                     help_text="The target user group that this notifications to be sent \
                                        to with is topic")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("system", "name"), name="notification_topic_unique_together_constraint")
        ]

    def __str__(self):
        return f"{self.name}"


class Coupon(StartAndExpireOnFieldMixin,
             AddedOnFieldMixin):
    """
    A coupon is a digital or paper with a unique code that has a specific value and is redeemed for 
    discount or other purposes
    """
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this coupon applies to",
                               related_name="coupons",
                               related_query_name="coupon")
    code = models.CharField("coupon code", unique=True, max_length=20, null=False, blank=True)
    discount_percentage_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    discount_fixed_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    total_use = models.PositiveIntegerField("total uses", default=1, help_text="How many times can be redeemed")
    use_count = models.PositiveIntegerField("use counts", default=0, help_text="How many times redeemed so far")
    # redeemed_on = models.DateTimeField("redemption date", default=timezone.now, editable=False)
    
    @property
    def is_active(self):
        if timezone.now() < self.expire_on:
            return True
        else:
            return False
        
    @property
    def is_all_used(self):
        if self.total_use == self.use_count:
            return True
        else:
            return False
        
    # def save(self, *args, **kwargs):
    #     kwargs["code"] = generate_coupon_code()
    #     print(kwargs)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code}"


class Voucher(StartAndExpireOnFieldMixin,
              AddedOnFieldMixin):  
    """
    A voucher is a digital or piece of paper with a unique code have a monetary value
    which can be exchanged for services on the system
    """
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this voucher applies to",
                               related_name="vouchers",
                               related_query_name="voucher")
    code = models.CharField("voucher code", unique=True, max_length=20, null=False, blank=True)
    initial_value = models.DecimalField("initial voucher value", default=0.00, decimal_places=5, max_digits=12)
    current_value = models.DecimalField("current voucher value", default=0.00, decimal_places=5, max_digits=12)
    base_currency = models.ForeignKey(Currency, 
                                      on_delete=models.CASCADE,
                                      related_name="vouchers",
                                      related_query_name="voucher",
                                      help_text="The default currency for this voucher.")
    @property
    def is_active(self)-> bool:
        if timezone.now() < self.expire_on:
            return True
        else:
            return False
        
    @property
    def has_balance(self) -> bool:
        if self.current_value > 0:
            return True
        else:
            return False

    def __str__(self):
        return self.code


class SupportedCardScheme(DescriptionAndAddedOnFieldMixin):
    """Card types that are supported by the system for online payment, such as Visa, Master Card, etc"""
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this supported card scheme applies to",
                               related_name="supported_card_schemes",
                               related_query_name="supported_card_scheme")
    name = models.CharField("card scheme name", max_length=50, null=False, blank=False, 
                            help_text="Card scheme name, such as Visa, Mastercard, etc")
    BIN = models.CharField("card BIN", max_length=19, null=False, blank=False, 
                           help_text="BIN is bank identification number that uniquely identifies the bank")

    def __str__(self):
        return f"{self.name}"
    


def get_system_asset_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"system/assets/{instance.asset_owner.name}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class SystemAssetOwner(DescriptionAndAddedOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this system asset owner belongs to",
                               related_name="system_asset_owners",
                               related_query_name="system_asset_owner")
    name = models.CharField("asset owner name", 
                            unique=True, 
                            max_length=250,
                            help_text = "name of asset owner, page name, component name, etc")

    def __str__(self):
        return self.name

class SystemAsset(DescriptionAndAddedOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this system asset belongs to",
                               related_name="system_assets",
                               related_query_name="system_asset")
    name = models.CharField("system asset name", max_length=100, blank=False, null=False)
    asset_owner = models.ForeignKey(SystemAssetOwner, 
                                    on_delete=models.CASCADE, 
                                    related_name="assets", 
                                    related_query_name="asset")
    asset_path = models.FileField("asset file path", upload_to=get_system_asset_path)
    
    def __str__(self):
        return "Owner: %s, Path: %s" % (self.asset_owner, self.name)


class ReferralRewardPlan(DescriptionAndAddedOnFieldMixin,
                         StartAndExpireOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this referral reward plan applies to",
                               related_name="referral_reward_plans",
                               related_query_name="referral_reward_plan")
    name = models.CharField("reward plan name", max_length=200, unique=True)
    referrer_reward_percentage_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    referrer_reward_fixed_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    referee_reward_percentage_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    referee_reward_fixed_value = models.DecimalField(decimal_places=2,  max_digits=10, default=0.00)
    number_of_referrals_needed = models.PositiveIntegerField(default=1, 
                                                             blank=True,
                                                             help_text="Number of referral actions needed to get the reward.")
    # reward_active_time_in_days = models.PositiveIntegerField(help_text="is the number of days that the reward stays active once awarded")

    def save(self, *args, **kwargs):
        # Check if there is already an unexpired reward plan for the system module
        existing_unexpired_reward_plan = ReferralRewardPlan.objects.filter(
            system=self.system,
            expire_on__gt = timezone.now()
        ).exclude(id=self.id).first()

        if (existing_unexpired_reward_plan and not self.id) or \
            (existing_unexpired_reward_plan and self.id and self.expire_on > timezone.now()):
            raise ValueError("A system module can only have one unexpired reward plan!")
        
        if self.start_on > self.expire_on:
            raise ValueError("Start date cannot be later than expire date!")
        
        
        super(ReferralRewardPlan, self).save(*args, **kwargs)


    @property
    def is_plan_active(self):
        return self.expire_on > timezone.now()

    def __str__(self):
        return f"{self.name}"
    

class FeaturingPrice(DescriptionAndAddedOnFieldMixin):
    system = models.ForeignKey(System, verbose_name="System Module", on_delete=models.CASCADE, 
                               help_text="The system module that this featuring price applies to",
                               related_name="featuring_prices",
                               related_query_name="featuring_price")
    price = models.DecimalField(decimal_places=5, max_digits=12, default=0.00000)
    base_currency = models.ForeignKey(Currency, 
                                      on_delete=models.CASCADE,
                                      related_name="featuring_prices",
                                      related_query_name="featuring_price",
                                      help_text="The default currency for this featuring price.")


    def __str__(self):
        return f"{self.price}"