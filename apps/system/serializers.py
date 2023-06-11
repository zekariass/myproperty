from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models as sys_models

#================ SYSTEM =============================
class SystemSerializer(ModelSerializer):
    class Meta:
        model = sys_models.System
        fields = "__all__"

#================ LISTING PARAMETER ===================
class ListingParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.ListingParameter
        fields = "__all__"

#================ SYSTEM PARAMETER ===================
class SystemParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemParameter
        fields = "__all__"

#================ CURRENCY ===========================
class CurrencySerializer(ModelSerializer):
    class Meta:
        model = sys_models.Currency
        fields = "__all__"


#================ PAYMENT METHOD =====================
class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = sys_models.PaymentMethod
        fields = "__all__"
        

#================ PAYMENT METHOD DISCOUNT ===============
class PaymentMethodDiscountSerializer(ModelSerializer):
    class Meta:
        model = sys_models.PaymentMethodDiscount
        fields = "__all__"


#================ DISCOUNT ===============================
class DiscountSerializer(ModelSerializer):
    class Meta:
        model = sys_models.Discount
        fields = "__all__"

    # def create(self, validated_data):
    #If is_trackable is True, then add a record to every agent in AgentDiscount table
    #     pass

    def validate(self, data):
        action = data.get("action")
        unit = data.get("unit")
        discount_type = data.get("discount_type")

        if (action == "COUNT" and unit == "SUBSCRIPTION") or \
            (action == "SINGLE" and unit in ["DAYS", "LISTINGS"]) or \
                (unit == "SUBSCRIPTION" and discount_type == "PAY_PER_LISTING") or \
                    (unit in ["DAYS", "LISTINGS"] and discount_type == "SUBSCRIPTION") or \
                        (action == "COUNT" and discount_type == "SUBSCRIPTION"):
            raise serializers.ValidationError({"error": "Action, unit and discount type incompatibility!"})

        return data
    
#================ SERVICE SUBSCRIPTION PLAN ===============
class ServiceSubscriptionPlanSerializer(ModelSerializer):
    class Meta:
        model = sys_models.ServiceSubscriptionPlan
        fields = "__all__"


#================SYSTEM RATING PLAN ===============
class SystemRatingSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemRating
        fields = "__all__"


#================SYSTEM FEEDBACK PLAN ===============
class SystemFeedbackSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemFeedback
        fields = "__all__"


#================ NOTIFICATION TOPIC ===============
class NotificationTopicSerializer(ModelSerializer):
    class Meta:
        model = sys_models.NotificationTopic
        fields = "__all__"
    
#================ COUPON ============================
class CouponSerializer(ModelSerializer):
    is_active = serializers.SerializerMethodField(read_only=True)
    is_all_used = serializers.SerializerMethodField(read_only=True)
    # system = SystemSerializer(read_only=True)
    class Meta:
        model = sys_models.Coupon
        fields = ["id", 
                  "system",
                  "code",
                  "discount_percentage_value", 
                  "discount_fixed_value", 
                  "total_use", 
                  "use_count", 
                  "is_active",
                  "is_all_used",
                  "start_on",
                  "expire_on",
                #   "added_on",
                  ]
        read_only_fields = ["id", "use_count", "code", "added_on"]

    def get_is_active(self, obj):
        return obj.is_active
    
    def get_is_all_used(self, obj):
        return obj.is_all_used
    
    def create(self, validated_data):
        from apps.mixins.functions import generate_unique_code
        from apps.mixins.constants import COUPON_CODE_LENGTH
        validated_data["code"] = generate_unique_code(COUPON_CODE_LENGTH)
        coupon = sys_models.Coupon.objects.create(**validated_data)
        return coupon

#================ VOUCHER ============================
class VoucherSerializer(ModelSerializer):
    is_active = serializers.SerializerMethodField(read_only=True)
    has_balance = serializers.SerializerMethodField(read_only=True)
    # system = SystemSerializer()
    class Meta:
        model = sys_models.Voucher
        fields = ["id", 
                  "system",
                  "code",
                  "initial_value",
                  "current_value",
                  "base_currency",
                  "has_balance",
                  "is_active",
                  "start_on",
                  "expire_on",
                #   "added_on"
                  ]
        
        read_only_fields = ["id", "code", "added_on", "current_value"]
    

    def get_is_active(self, obj):
        return obj.is_active
    
    def get_has_balance(self, obj):
        return obj.has_balance
    
    def create(self, validated_data):
        from apps.mixins.functions import generate_unique_code
        from apps.mixins.constants import VOUCHER_CODE_LENGTH
        validated_data["code"] = generate_unique_code(VOUCHER_CODE_LENGTH)
        validated_data["current_value"] = validated_data["initial_value"] 
        voucher = sys_models.Voucher.objects.create(**validated_data)
        return voucher
    
#================ SUPPORTED CARD SCHEME ===============
class SupportedCardSchemeSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SupportedCardScheme
        fields = "__all__"

#================ SYSTEM ASSET OWNER ===================
class SystemAssetOwnerSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemAssetOwner
        fields = "__all__"

#================ SYSTEM ASSET =========================
class SystemAssetSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemAsset
        fields = "__all__"

#=============== REFERAL REWARD PLAN =========================
class ReferralRewardPlanSerializer(ModelSerializer):
    is_plan_active = serializers.SerializerMethodField()
    class Meta:
        model = sys_models.ReferralRewardPlan
        fields = ["id", 
                  "system", 
                  "name", 
                  "referrer_reward_percentage_value",
                  "referrer_reward_fixed_value",
                  "referee_reward_percentage_value",
                  "referee_reward_fixed_value",
                  "number_of_referrals_needed",
                  "start_on",
                  "expire_on",
                  "is_plan_active",
                  "added_on"]
        read_only_fields = ["id", "is_plan_active", "added_on"]
        # extra_kwargs = {
        #     "is_active": {
        #         "read_only": True
        #     }
        # }

    def get_is_plan_active(self, obj):
        return obj.is_plan_active


#=============== FEATURING PRICE =============================
class FeaturingPriceSerializer(ModelSerializer):
    class Meta:
        model = sys_models.FeaturingPrice
        fields = "__all__"
