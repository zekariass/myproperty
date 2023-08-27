from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.mixins import constants

from . import models


# ========================= PERMISSION ====================================
class PermissionSerializer(ModelSerializer):
    """
    Serialize and deserialize Permission object
    """

    class Meta:
        model = Permission
        fields = ["name", "codename"]
        read_only_fields = ["name", "codename"]


# ========================= USER GROUP ====================================
class UserGroupSerializer(ModelSerializer):
    """
    Serialize and User Group user object
    """

    permissions = PermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ("name", "permissions")


# ========================= ROLE ====================================
class RoleSerializer(ModelSerializer):
    """
    Serialize and deserialize Role object
    """

    class Meta:
        model = models.Role
        fields = ["name", "group", "permissions", "added_on"]


# ========================= USER ====================================
class MypropertyUserSerializer(ModelSerializer):
    """
    Serialize and deserialize user object
    """

    groups = UserGroupSerializer(read_only=True, many=True)
    permissions = PermissionSerializer(read_only=True, many=True)
    roles = RoleSerializer(read_only=True, many=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "registered_on",
            "permissions",
            "groups",
            "roles",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        groups = Group.objects.all()
        is_staff = validated_data.get("is_staff")
        if is_staff is None or is_staff is False:
            user_group = groups.get(name=constants.USER_GROUP_ANY)
        else:
            user_group = groups.get(name=constants.USER_GROUP_ADMIN)

        user = get_user_model().objects.create(**validated_data)
        user.groups.add(user_group)

        user.set_password(password)
        user.save()
        return user


class MypropertyUserNoPasswordSerializer(ModelSerializer):
    """User update serializer. Password is not directly changed by using
    user profile change. Rather it has dedicated Password change view with its
    Serializer"""

    groups = UserGroupSerializer(read_only=True, many=True)
    permissions = PermissionSerializer(read_only=True, many=True)
    roles = RoleSerializer(read_only=True, many=True)

    def update(self, instance, validated_data):
        """Update User Object"""
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.middle_name = validated_data.get("middle_name", instance.middle_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
            "registered_on",
            "permissions",
            "groups",
            "roles",
        ]
        read_only_fields = [
            "id",
            "is_superuser",
            "is_staff",
            "registered_on",
            "is_active",
        ]


# class ChangeUserPasswordSerializer(serializers.Serializer):
#     """Password change serializer. It shows only new and old password fields"""

#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#     # confirm_password = serializers.CharField(required=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    """Password reset request serializer"""

    email = serializers.EmailField(required=True)
    reset_url = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    """Password reset request serializer"""

    # old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    login_url = serializers.CharField(required=True)
