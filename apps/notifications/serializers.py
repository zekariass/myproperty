from rest_framework import serializers

from . import models as notif_models


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notif_models.UserNotification
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = notif_models.UserNotificationPreference
        fields = "__all__"
        read_only_fields = ["id", "user", "added_on"]


class UserNotificationChannelPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = notif_models.UserNotificationChannelPreference
        fields = "__all__"
        read_only_fields = ["id", "user", "added_on"]


class AgentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = notif_models.AgentNotification
        fields = "__all__"
        # read_only_fields = ["id", "agent"]


class AgentNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = notif_models.AgentNotificationPreference
        fields = "__all__"
        read_only_fields = ["id", "agent", "added_on"]


class AgentNotificationChannelPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = notif_models.AgentNotificationChannelPreference
        fields = "__all__"
        read_only_fields = ["id", "agent", "added_on"]
