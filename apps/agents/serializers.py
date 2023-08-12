from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# from apps.agents.tasks import (
#     send_new_agent_branch_added_email_to_agent,
#     send_welcome_email_to_new_agent,
# )
from apps.system.serializers import PaymentMethodDiscountSerializer

from . import models as agent_models
from apps.commons.models import Address
from apps.commons.serializers import AddressSerializer

from apps.users.serializers import UserGroupSerializer
from apps.system import models as sys_models

from apps.mixins.functions import (
    generate_agent_branch_code,
    generate_agent_referral_code,
    send_new_agent_created_email,
)
from apps.mixins.constants import USER_GROUP_AGENT, AGENT_REFERRAL_CODE_INITIAL

# ================= AGENT ===================================

# AGENT BRANCH FOR MAIN BRANCH CREATION


class AgentMainBranchSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = agent_models.AgentBranch
        fields = [
            "id",
            "branch_code",
            "name",
            "email",
            "phone_number",
            "address",
            "is_main_branch",
        ]
        read_only_fields = ["id", "is_main_branch", "branch_code"]

    def create(self, validated_data):
        branch_code = generate_agent_branch_code()
        branch_instance = agent_models.AgentBranch.objects.create(
            branch_code=branch_code, **validated_data
        )
        return branch_instance


class AgentCreateSerializer(ModelSerializer):
    agent_branch = AgentMainBranchSerializer(write_only=True)
    user_group = UserGroupSerializer(read_only=True)

    class Meta:
        model = agent_models.Agent
        fields = [
            "id",
            "name",
            "motto",
            "logo_path",
            "referral_code",
            "user_group",
            "agent_branch",
            "referred_by",
        ]
        read_only_fields = ["id", "referral_code", "referred_by"]

    def create(self, validated_data):
        # GENERATE AGENT REFERRAL CODE
        referral_code = generate_agent_referral_code()

        query_params = self.context["request"].query_params
        referrer_code = None
        if "referred_by" in query_params:
            referrer_code = query_params["referred_by"]

        user = self.context.get("request").user

        # GET AGENT MAIN BRANCH DATA
        agent_main_branch_data = validated_data.pop("agent_branch")

        # GET ADDRESS DATA
        address = agent_main_branch_data.pop("address")
        with transaction.atomic():
            try:
                # GET USER GROUP
                user_group = Group.objects.get(name=USER_GROUP_AGENT)

                # GET REFERRE AGENT IF AGENT IS REFERRED BY ANOTHER AGENT
                referrer_agent = None
                if referrer_code and referrer_code.startswith(
                    AGENT_REFERRAL_CODE_INITIAL
                ):
                    referrer_agent = agent_models.Agent.objects.filter(
                        referral_code=referrer_code
                    ).first()

                # CREATE AGENT
                agent = agent_models.Agent.objects.create(
                    user_group=user_group,
                    referral_code=referral_code,
                    referred_by=referrer_agent if referrer_agent else None,
                    **validated_data,
                )

                # CREATE ADDRESS FOR THE BRANCH
                address = Address.objects.create(**address)

                # CREATE MAIN BRANCH
                # MAIN BRANCH IS CREATED DURING FIRST AGENT REGISTRATION AUTOMATICALLY
                branch_code = generate_agent_branch_code()
                branch = agent_models.AgentBranch.objects.create(
                    agent=agent,
                    branch_code=branch_code,
                    is_main_branch=True,
                    address=address,
                    **agent_main_branch_data,
                )

                # SET THE CURRENT USER WHO CREATE THE AGENT AS SUPER ADMIN OF THE AGENT
                agent_models.AgentAdmin.objects.create(
                    agent_branch=branch, user=user, is_superadmin=True
                )

                # SEND NEW AGENT ADDED EMAIL
                # send_welcome_email_to_new_agent.delay(
                #     agent_branch=branch.id,
                # )

                # CHECK AGENT MODEL POST SAVE SIGNAL RECIEVER METHOD FOR REFERRAL CREATION

            except Exception as e:
                raise e

        return agent


class AgentSerializer(ModelSerializer):
    agent_branch = AgentMainBranchSerializer(
        source="branches", read_only=True, many=True
    )
    user_group = UserGroupSerializer(read_only=True)
    detail = serializers.HyperlinkedIdentityField(
        view_name="retrieve-update-destroy-agent", lookup_field="pk"
    )
    # has_active_subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = agent_models.Agent
        fields = [
            "id",
            "detail",
            "name",
            "motto",
            "logo_path",
            "referral_code",
            "has_active_subscription",
            "user_group",
            "agent_branch",
            "referred_by",
        ]
        read_only_fields = [
            "id",
            "referral_code",
            "agent_branch",
            "referred_by",
            "has_active_subscription",
        ]


# ================= AGENT BRANCH =============================
class AgentBranchSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = agent_models.AgentBranch
        fields = [
            "id",
            "agent",
            "name",
            "email",
            "phone_number",
            "is_main_branch",
            "branch_code",
            "address",
        ]
        read_only_fields = ["id", "agent", "branch_code"]

    def create(self, validated_data):
        with transaction.atomic():
            try:
                # GET AGENT ID FROM KWARGS WHICH IS SET IN THE URL
                agent_id = self.context["request"].parser_context["kwargs"].get("pk")

                # GET AGENT
                agent = agent_models.Agent.objects.get(pk=agent_id)

                validated_data["branch_code"] = generate_agent_branch_code()

                # POP ADDRESS DATA
                address = validated_data.pop("address")

                # CREATE ADRESS
                address = Address.objects.create(**address)

                # CREATE AGENT BRANCH
                agent_branch = agent_models.AgentBranch.objects.create(
                    address=address,
                    agent=agent,
                    **validated_data,
                )

                # SEND NEW AGENT ADDED EMAIL
                # send_new_agent_branch_added_email_to_agent.delay(
                #     agent_branch=agent_branch.id,
                # )

                return agent_branch
            except Exception as e:
                raise e

    def update(self, instance, validated_data):
        address = validated_data.pop("address")
        with transaction.atomic():
            try:
                # UPDATE BRANCH
                instance.name = validated_data.get("name", instance.name)
                instance.phone_number = validated_data.get(
                    "phone_number", instance.name
                )
                instance.email = validated_data.get("email", instance.name)
                instance.is_main_branch = validated_data.get(
                    "is_main_branch", instance.name
                )

                # SAVE BRANCH
                instance.save()

                # UPDATE ADDRESS
                instance.address.street = address.get("street", instance.address.street)
                instance.address.post_code = address.get(
                    "post_code", instance.address.post_code
                )
                instance.address.house_number = address.get(
                    "house_number", instance.address.house_number
                )
                instance.address.city = address.get("city", instance.address.city)
                instance.address.region = address.get("region", instance.address.region)
                instance.address.latitude = address.get(
                    "latitude", instance.address.latitude
                )
                instance.address.longitude = address.get(
                    "longitude", instance.address.longitude
                )
                instance.address.country = address.get(
                    "country", instance.address.country
                )

                # SAVE ADDRESS
                instance.address.save()
            except Exception as e:
                raise e
        return instance


# ================= AGENT ADMIN =============================


class AgentAdminSerializer(ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    user = serializers.SlugRelatedField(slug_field="first_name", read_only=True)
    agent_branch = serializers.HyperlinkedRelatedField(
        view_name="retrieve-update-destroy-agentbranch",
        queryset=agent_models.AgentAdmin.objects.all(),
    )

    class Meta:
        model = agent_models.AgentAdmin
        fields = ["id", "agent_branch", "user", "user_email", "is_superadmin"]
        read_only_fields = ["id", "agent_branch", "user"]

    def create(self, validated_data):
        # print(validated_data)
        user_email = validated_data.pop("user_email")
        try:
            user = get_user_model().objects.get(email=user_email)
        except get_user_model().DoesNotExist:
            return ObjectDoesNotExist(
                {"result": f"No user registered with {user_email} found."}
            )

        try:
            branch_id = self.context["request"].parser_context["kwargs"].get("pk")
            agent_branch = agent_models.AgentBranch.objects.get(pk=branch_id)
        except agent_models.AgentBranch.DoesNotExist:
            return ObjectDoesNotExist({"result": f"{agent_branch} not found."})

        else:
            instance = agent_models.AgentAdmin.objects.create(
                user=user, agent_branch=agent_branch, **validated_data
            )
            return instance


class AgentAdminRetrieveUpdateDestroySerializer(ModelSerializer):
    agent_branch = serializers.HyperlinkedRelatedField(
        view_name="retrieve-update-destroy-agentbranch",
        queryset=agent_models.AgentAdmin.objects.all(),
    )

    class Meta:
        model = agent_models.AgentAdmin
        fields = ["id", "agent_branch", "user", "is_superadmin"]
        read_only_fields = ["id", "user"]


# ================= AGENT DISCOUNT =============================
class AgentDiscountSerializer(ModelSerializer):
    class Meta:
        model = agent_models.AgentDiscountTracker
        fields = "__all__"


# ================= AGENT SERVICE SUBSCRIPTION ==================
class AgentServiceSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = agent_models.AgentServiceSubscription
        fields = "__all__"


# ================= AGENT REFERRAL TRACKER ======================
class AgentReferralTrackerSerializer(ModelSerializer):
    class Meta:
        model = agent_models.AgentReferralTracker
        fields = "__all__"


# ================= AGENT REFERRAL ===============================
class AgentReferralSerializer(ModelSerializer):
    class Meta:
        model = agent_models.AgentReferral
        fields = "__all__"


# ================= AGENT REFERRAL REWARD =========================
class AgentReferralRewardSerializer(ModelSerializer):
    class Meta:
        model = agent_models.AgentReferralReward
        fields = "__all__"


# ================= REQUESTER ======================================
class RequesterSerializer(ModelSerializer):
    class Meta:
        model = agent_models.Requester
        fields = "__all__"
        read_only_fields = ["user"]


# ================= REQUEST =========================================


class InlineRequestMessageSerializer(ModelSerializer):
    class Meta:
        model = agent_models.RequestMessage
        fields = "__all__"


class RequestSerializer(ModelSerializer):
    requester = RequesterSerializer(read_only=True)
    messages = InlineRequestMessageSerializer(read_only=True, many=True)

    class Meta:
        model = agent_models.Request
        fields = [
            "id",
            "requester",
            "agent_branch",
            "listing",
            "request_type",
            "added_on",
            "messages",
        ]
        read_only_fields = ["id", "requester", "added_on"]

    # def get_messages(self, obj):
    #     return InlineRequestMessageSerializer(
    #         instance=obj.requestmessage_set.all()
    #     ).data

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation["messages"] = instance.requestmessage_set.all()
    #     return representation


# ================= REQUEST MESSAGE ==================================
class RequestMessageSerializer(ModelSerializer):
    request = RequestSerializer(read_only=True)

    class Meta:
        model = agent_models.RequestMessage
        fields = "__all__"
        read_only_fields = ["request"]


# ================= AGENT CALCULATED DISCOUNT ==================================
class AgentCalculatedDiscountSerializer(serializers.Serializer):
    listing_discount = serializers.SerializerMethodField(read_only=True)
    payment_method_discounts = PaymentMethodDiscountSerializer(read_only=True)

    class Meta:
        fields = ["listing_discount", "payment_method_discounts"]

    def get_listing_discount(self, obj):
        return "1233"
