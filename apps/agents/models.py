import os
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.db.models import F
from django.db import transaction
from django.dispatch import receiver

from django.contrib.auth.models import Group
from django.utils import timezone
from django.conf import settings

from apps.commons import models as cmns_models
from apps.mixins import constants
from apps.system import models as sys_models


from apps.mixins.common_fields import (
    AddedOnFieldMixin,
    DescriptionAndAddedOnFieldMixin,
    ExpireOnFieldMixin,
    StartAndExpireOnFieldMixin,
)
from apps.mixins.functions import (
    generate_coupon_code,
    create_coupon,
)
from apps.mixins.constants import (
    REQUESTER_REQUEST_TYPES,
    REQUEST_MESSAGE_SENDERS,
    SYSTEM_MODULE_NAME_MYPROPERY,
    LISTING_PARAM_AGENT_REFERRAL_COUPON_MAX_USE,
)


def create_agent_logo_file_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    file_path = (
        f"agents/logo/{instance.pk}_{now:%Y%m%d%H%M%S}_{milliseconds}{extension}"
    )
    return file_path


class Agent(DescriptionAndAddedOnFieldMixin):
    """Agent is a company that list properties to the system"""

    name = models.CharField(
        verbose_name="agent name", max_length=200, blank=False, null=False
    )
    motto = models.CharField(
        verbose_name="agent slogan", max_length=100, null=True, blank=True
    )
    logo_path = models.ImageField(
        "company logo", upload_to=create_agent_logo_file_path, null=True, blank=True
    )
    referral_code = models.CharField(
        "agent referral code", max_length=15, unique=True, db_index=True
    )
    referred_by = models.ForeignKey(
        "self",
        verbose_name="referrer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user_group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="category of user group",
        related_name="agents",
        related_query_name="agent",
    )

    def __str__(self):
        return f"{self.id} {self.name}"

    @property
    def has_active_subscription(self):
        return len(self.service_subscriptions.filter(expire_on__gt=timezone.now())) >= 1


@receiver(post_save, sender=Agent)
def agent_post_save(sender, instance, created, **kwargs):
    if created and instance.referred_by is not None:
        from apps.agents import tasks

        referrer_agent = instance.referred_by
        # CREATE REFERRAL
        # CHECK IF THERE IS PLAN FOR MYPROPERTY MODULE
        referrer_coupon = None
        referee_coupon = None
        with transaction.atomic():
            # CHECK IF REFERRAL REWARD PLAN IS AVAILABLE
            available_reward_plan = sys_models.ReferralRewardPlan.objects.filter(
                expire_on__gt=timezone.now(),
                system__name=SYSTEM_MODULE_NAME_MYPROPERY,
            ).first()

            if available_reward_plan:
                # CREATE OR UPDATE AGENT REFERRAL TRACKER
                # IF THERE IS TRACKER WITH is_open=True, UPDATE IT, OTHERWISE CREATE NEW
                (
                    referral_tracker_obj,
                    new_created,
                ) = AgentReferralTracker.objects.update_or_create(
                    defaults={
                        "agent": referrer_agent,
                        "referral_reward_plan": available_reward_plan,
                        "is_open": True,
                    },
                    referral_reward_plan=available_reward_plan,
                    is_open=True,
                    agent=referrer_agent,
                )

                # IF NEW TRACKER IS CREATED, SET THE CURRENT REFERRALS TO 1
                if not new_created:
                    AgentReferralTracker.objects.filter(
                        pk=referral_tracker_obj.id
                    ).update(num_of_current_referrals=F("num_of_current_referrals") + 1)

                # CREATE AGENT REFERRAL
                AgentReferral.objects.create(
                    referrer_agent=referrer_agent,
                    referee_agent=instance,
                    referral_tracker=referral_tracker_obj,
                )

                # GET THE SYSTEM MODULE
                system = (
                    sys_models.System.objects.filter(
                        name=SYSTEM_MODULE_NAME_MYPROPERY
                    ).first()
                    or None
                )

                # CREATE COUPON BASED ON values FIELD OF ListingParameter AND
                # PERCENTAGE AND FIXED VALUES OF ReferralRewardPlan
                referrer_discount_percentage_value = (
                    available_reward_plan.referrer_reward_percentage_value
                )
                referrer_discount_fixed_value = (
                    available_reward_plan.referrer_reward_fixed_value
                )

                referee_discount_percentage_value = (
                    available_reward_plan.referee_reward_percentage_value
                )
                referee_discount_fixed_value = (
                    available_reward_plan.referee_reward_fixed_value
                )

                # GET AGENT REFERRAL COUPON MAX USE LISTING PARAMETER
                listing_param_for_agent_referral_coupon = (
                    sys_models.ListingParameter.objects.filter(
                        name=LISTING_PARAM_AGENT_REFERRAL_COUPON_MAX_USE
                    ).first()
                )

                coupon_total_use = 1
                if (
                    listing_param_for_agent_referral_coupon
                    and listing_param_for_agent_referral_coupon.is_active
                ):
                    coupon_total_use = int(
                        listing_param_for_agent_referral_coupon.value
                    )

                # THE LIFE TIME OF THE COUPON. IT IS THE NUMBER OF DAYS THE COUPON STAY VALID
                coupon_life_time = 1

                coupon_life_time_sys_param_instance = (
                    sys_models.SystemParameter.objects.filter(
                        name=constants.SYSTEM_PARAM_COUPON_LIFE_TIME
                    )
                )

                if coupon_life_time_sys_param_instance.exists():
                    coupon_life_time = int(
                        coupon_life_time_sys_param_instance.first().value
                    )

                # CREATE COUPON FOR REFEREE AGENT
                if (
                    referee_discount_percentage_value > 0
                    or referee_discount_fixed_value > 0
                ):
                    referee_coupon_code = generate_coupon_code()
                    referee_coupon = create_coupon(
                        sys_models.Coupon,
                        code=referee_coupon_code,
                        discount_percentage_value=referee_discount_percentage_value,
                        discount_fixed_value=referee_discount_fixed_value,
                        total_use=coupon_total_use,
                        use_count=0,
                        expire_on=timezone.now()
                        + datetime.timedelta(days=coupon_life_time),
                        system=system,
                    )

                    # EMAIL THE CODE TO RFEREE AND REFERRER
                    if referee_coupon is not None:
                        tasks.send_referee_coupon_email.delay(
                            referee_coupon=referee_coupon_code,
                            percentage_value=referee_discount_percentage_value,
                            fixed_value=referee_discount_fixed_value,
                            agent_id=instance.id,
                        )

                # GET THE NEW OR UPDATE AGENT REFERRAL TRACKER OBJECT
                post_save_referral_tracker_state = AgentReferralTracker.objects.filter(
                    pk=referral_tracker_obj.id
                )

                # CREATE REFERER COUPON IF REFERER HAS REFERRED ENOUGH REFERRALS TO BE REWARDED
                if (
                    post_save_referral_tracker_state.first().num_of_current_referrals
                    == post_save_referral_tracker_state.first().referral_reward_plan.number_of_referrals_needed
                ):
                    # GENERATE COUPON CODE
                    referrer_coupon_code = generate_coupon_code()

                    # CREATE REFERRER COUPON
                    referrer_coupon = create_coupon(
                        sys_models.Coupon,
                        code=referrer_coupon_code,
                        discount_percentage_value=referrer_discount_percentage_value,
                        discount_fixed_value=referrer_discount_fixed_value,
                        total_use=coupon_total_use,
                        use_count=0,
                        expire_on=timezone.now()
                        + datetime.timedelta(days=coupon_life_time),
                        # listing_parameter = listing_param_for_agent_referral_coupon,
                        system=system,
                    )

                    # SET is_open VALUE OF REFERRAL TRACKER TO FALSE
                    if referrer_coupon:
                        post_save_referral_tracker_state.update(is_open=False)

                        # EMAIL THE CODE TO REFERRER
                        tasks.send_referrer_coupon_email.delay(
                            referrer_coupon=referrer_coupon_code,
                            percentage_value=referrer_discount_percentage_value,
                            fixed_value=referee_discount_fixed_value,
                            agent_id=referrer_agent.id,
                        )


class AgentBranch(DescriptionAndAddedOnFieldMixin):
    """Agent branch. One agent may have more than offices and each office is a branch"""

    agent = models.ForeignKey(
        Agent,
        verbose_name="parent agent",
        on_delete=models.CASCADE,
        related_name="branches",
        related_query_name="branch",
    )
    branch_code = models.CharField(
        "agent branch code", max_length=15, unique=True, db_index=True
    )
    name = models.CharField("agent branch name", max_length=100)
    is_main_branch = models.BooleanField(
        "is this the main branch of the agent", default=False
    )
    email = models.EmailField("branch email address", max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.ForeignKey(
        cmns_models.Address,
        verbose_name="agent branch address",
        on_delete=models.SET_NULL,
        null=True,
        related_name="agent_branches",
        related_query_name="agent_branch",
    )

    class Meta:
        verbose_name_plural = "Agent branches"
        constraints = [
            # ONLY UNIQUE BRANCH NAME PER AGENT
            models.UniqueConstraint(
                fields=["agent", "name"], name="unique_branch_name_per_agent_branch"
            ),
            # ONLY ONE MAIN BRANCH PER AGENT
            models.UniqueConstraint(
                fields=["agent"],
                condition=models.Q(is_main_branch=True),
                name="only_single_mainbranch_per_agent",
            ),
        ]

    def clean(self):
        super().clean()
        if (
            self.is_main_branch
            and self.agent.branches.filter(is_main_branch=True)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError("An agent can have only one main branch!")

    def create(self, **kwargs):
        self.full_clean()
        return super().create(**kwargs)

    def __str__(self):
        return f"{self.id} {self.name} {self.branch_code}"


class AgentAdmin(AddedOnFieldMixin):
    """AgentAdmin is a user that works as a staff or admin in the agent company"""

    agent_branch = models.ForeignKey(
        AgentBranch,
        help_text="The agent branch that this user works in",
        on_delete=models.CASCADE,
        related_name="branch_admins",
        related_query_name="branch_admin",
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="user admin",
        on_delete=models.CASCADE,
        related_name="agent_branch",
        help_text="The user that works as admin in the agent branch",
        error_messages={
            "user_not_unique": "A user can create only one agent or \
                                             must be assigned to a single agent as admin"
        },
    )
    is_superadmin = models.BooleanField(
        default=False, help_text="Is this user the super administrator of the branch?"
    )

    def __str__(self):
        return f"{self.user.first_name}"


# TODO TO HANDLE IN PROPERTY LISTING APP


class AgentDiscountTracker(AddedOnFieldMixin, StartAndExpireOnFieldMixin):
    """Trackable discount of an agent"""

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="discounts",
        related_query_name="discount",
    )
    discount = models.ForeignKey(
        sys_models.Discount,
        on_delete=models.CASCADE,
        help_text="parent discount configuration that this discount is based from",
        related_name="agent_discounts",
        related_query_name="agent_discount",
    )
    used_discounts = models.PositiveIntegerField(
        "how many discounts used so far?", default=0
    )
    max_discounts = models.PositiveIntegerField(
        "how many total discounts you have?", default=0
    )

    def __str__(self) -> str:
        return f"Agent: {self.agent.name}, Discount: {self.discount.name}, max: {self.max_discounts}, used: {self.used_discounts}"


class AgentReferralTracker(AddedOnFieldMixin):
    """Agent referral tracker. It tracks the number of referrals needed with
    number of current referrals acheived so far. If both values equal,
    the reward will be awarded at the time of the last referral action"""

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="referral_trackers",
        related_query_name="referral_tracker",
    )
    # num_of_referrals_needed = models.PositiveIntegerField("number of referrals needed?",
    #                                                       help_text="The number of referrals needed to get the reward.",
    #                                                       default = 1)
    num_of_current_referrals = models.PositiveIntegerField(
        "current number of referrals?", default=1
    )
    referral_reward_plan = models.ForeignKey(
        sys_models.ReferralRewardPlan,
        help_text="The reward plan that this tracker is based on",
        on_delete=models.CASCADE,
        related_name="agent_referral_trackers",
        related_query_name="agent_referral_tracker",
    )
    is_open = models.BooleanField(
        "is tracker open?",
        default=True,
        help_text="Does the agent have open/anawarded reward tracker?",
    )

    @property
    def is_rewarded(self):
        return (
            self.num_of_current_referrals
            == self.referral_reward_plan.number_of_referrals_needed
        )

    def __str__(self):
        return f"{self.agent.name}, Current referrals={self.num_of_current_referrals}, Referrals_needed={self.referral_reward_plan.number_of_referrals_needed}"


# receiver(post_save, sender=AgentReferralTracker)
# def agent_referral_tracker_post_save(sender, instance, created, **kwargs):
#     print("=======================================>: ", instance.num_of_current_referrals)


class AgentReferral(AddedOnFieldMixin):
    """Agent referral system model. It records each referrals the agent perform"""

    referrer_agent = models.ForeignKey(
        Agent,
        help_text="An agent who referred another agent",
        on_delete=models.CASCADE,
        related_name="referrals",
        related_query_name="referral",
    )
    referee_agent = models.ForeignKey(
        Agent, help_text="An agent referred by another agent", on_delete=models.CASCADE
    )
    referral_tracker = models.ForeignKey(
        AgentReferralTracker,
        on_delete=models.CASCADE,
        related_name="agent_referrals",
        related_query_name="agent_referral",
    )

    def __str__(self):
        return f"Referrer: {self.referrer_agent}, Referee: {self.referee_agent}"


class AgentReferralReward(AddedOnFieldMixin):
    """The reward that is awarded to the referrer or referee agent"""

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="referral_rewards",
        related_query_name="referral_reward",
    )
    referral_tracker = models.ForeignKey(
        AgentReferralTracker,
        on_delete=models.CASCADE,
        related_name="rewards",
        related_query_name="reward",
    )
    coupon = models.ForeignKey(
        sys_models.Coupon,
        on_delete=models.CASCADE,
        help_text="The coupon that is rewarded to the agent",
    )
    is_referee_reward = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.coupon.code}"


class AgentServiceSubscription(AddedOnFieldMixin, ExpireOnFieldMixin):
    """Subscriptions that the agent has subscribed to the system"""

    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name="service_subscriptions",
        related_query_name="service_subscription",
    )
    subscription_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="It is the actual payable price after discounts are deducted. The original price is the price at ServiceSubscriptionPlan",
    )
    # subscription_currency = models.ForeignKey(
    #     sys_models.Currency, on_delete=models.SET_NULL, null=True
    # )
    subscription_plan = models.ForeignKey(
        sys_models.ServiceSubscriptionPlan, on_delete=models.SET_NULL, null=True
    )
    payment = models.ForeignKey(
        "payments.Payment", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def has_active_subscription(self):
        return self.expire_on > timezone.now() and self.payment.is_approved

    def __str__(self):
        return f"{self.agent.name}: {self.subscription_price}"


class Requester(AddedOnFieldMixin):
    """Requester that the sends the request to the agent"""

    first_name = models.CharField("requester first name", max_length=50)
    middle_name = models.CharField(
        "requester middle name", max_length=50, null=True, blank=True
    )
    last_name = models.CharField("requester last name", max_length=50)
    email = models.EmailField("requester email address", max_length=100)
    phone_number = models.CharField("requester phone number", max_length=15)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests",
        related_query_name="request",
        help_text="This value becomes null when the requester is anonymous user",
    )

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"


class Request(AddedOnFieldMixin):
    """The request that the requester client/user send to the agent"""

    agent_branch = models.ForeignKey(
        AgentBranch,
        on_delete=models.CASCADE,
        related_name="agent_requests",
        related_query_name="agent_request",
        help_text="The agent branch that the request is sent to",
    )
    listing = models.ForeignKey(
        "listings.Listing",
        on_delete=models.CASCADE,
        related_name="requests",
        related_query_name="request",
    )
    requester = models.ForeignKey(
        Requester,
        on_delete=models.CASCADE,
        related_name="user_requests",
        related_query_name="user_request",
        help_text="The user that the request is sent by",
    )
    request_type = models.CharField(
        "type of request", max_length=100, choices=REQUESTER_REQUEST_TYPES
    )

    def __str__(self):
        return f"{self.id} {self.request_type}"


class RequestMessage(AddedOnFieldMixin):
    """This is the message associated with the request. All messages with in same
    thread or conversation will have same request ID as a reference to the request.
    This class has the following properties"""

    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name="messages"
    )
    message = models.TextField()
    sender = models.CharField(
        "message sender", max_length=100, choices=REQUEST_MESSAGE_SENDERS
    )

    def __str__(self):
        return f"{self.id} {self.sender}"
