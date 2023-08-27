from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import TimestampSigner
from django.core.cache import cache
from django.urls import reverse

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    CreateAPIView,
    ListAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.mixins import constants

from apps.mixins.functions import get_success_response_dict, get_error_response_dict
from apps.system.models import SystemParameter
from apps.users import tasks

from . import serializers as auth_serializers
from . import models as auth_models


# =============Roles==============================================================
class RoleListCreateView(ListCreateAPIView):
    """
    Create and Update Roles. This view checks if the user is Admin. Oly admin users can
    create and see list of Roles.

    """

    queryset = auth_models.Role.objects.all()
    serializer_class = auth_serializers.RoleSerializer


class RoleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete a Role. This view checks if the user is Admin. Oly admin users can
    these operations on Roles"""

    queryset = auth_models.Role.objects.all()
    serializer_class = auth_serializers.RoleSerializer


# =============Groups==============================================================
class GroupListCreateView(ListCreateAPIView):
    """Create and Update groups. This view checks if the user is Admin. Oly admin users can
    create and see list of groups

    The Following are groups names used: \n
        1. SYSTEM_ADMIN
        2. AGENT
        3. ANY
    """

    queryset = Group.objects.all()
    serializer_class = auth_serializers.UserGroupSerializer
    permission_classes = (IsAdminUser,)


class GroupRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete a group. This view checks if the user is Admin. Oly admin users can
    these operations on groups"""

    queryset = Group.objects.all()
    serializer_class = auth_serializers.UserGroupSerializer
    permission_classes = (IsAdminUser,)


# =============Users==============================================================


class UserCreateView(CreateAPIView):
    """Create User View. This view does not need the user to be authenicated to create user"""

    queryset = get_user_model().objects.all()
    serializer_class = auth_serializers.MypropertyUserSerializer


class UserListView(ListAPIView):
    """List users of the system. This view checks if the user is Admin. Oly admin users can
    see list of users"""

    queryset = get_user_model().objects.all()
    serializer_class = auth_serializers.MypropertyUserSerializer
    permission_classes = [IsAdminUser]


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """This view is used to retrieve, delete and update a user. User need to be authenticated
    to be able to do these operations."""

    queryset = get_user_model().objects.all()
    serializer_class = auth_serializers.MypropertyUserNoPasswordSerializer
    permission_classes = (IsAuthenticated,)


# class ChangeUserPasswordView(UpdateAPIView):
#     """Password Change. The user need to be authenticated to change password"""

#     serializer_class = auth_serializers.ChangeUserPasswordSerializer
#     permission_classes = (IsAuthenticated,)

#     def update(self, request, *args, **kwargs):
#         user = request.user
#         serializer = self.get_serializer(data=request.data)

#         serializer.is_valid(raise_exception=True)

#         # Check old password
#         if not user.check_password(serializer.data.get("old_password")):
#             return Response(
#                 get_error_response_dict(message="Wrong old password!"),
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Change password
#         user.set_password(serializer.data.get("new_password"))
#         user.save()

#         # Update the session has to prevent the user from being logged out
#         update_session_auth_hash(request, user)

#         return Response(
#             get_success_response_dict(message="Password Changed!"),
#             status=status.HTTP_200_OK,
#         )


class PasswordResetRequestView(APIView):
    """Password Reset. This view can be used for authenticated user and lost password"""

    serializer_class = auth_serializers.PasswordResetRequestSerializer

    def post(self, request):
        user_email = request.data["email"]
        reset_url = request.data["reset_url"]

        user = None

        # CHECK IF USER IS AUTHENTICATED
        if not request.user.is_authenticated:
            try:
                # GET THE USER FROM DB IF THE USER IS NOT AUTHENTICATED
                user = get_user_model().objects.get(email=user_email)
            except ObjectDoesNotExist:
                return Response(
                    get_error_response_dict(
                        message=f"User with email {user_email} does not exist"
                    )
                )
        else:
            # GET THE USER FROM REQUEST IF ALREADY AUTHENTICATED
            user = request.user

        user_email = user.email

        # SIGN THE USER EMAIL AND SAVE IT TO CACHE
        # THIS WILL BE VERIFIED LATER WHEN THE USER RESETS THE PASSWORD
        signer = TimestampSigner()
        signed_email = signer.sign(user_email)

        # CONSTRUCT RESET URL TO BE SENT TO THE USERS EMAIL
        # base_url = request.build_absolute_uri(reverse("user-password-reset"))
        pass_reset_url = reset_url + "?reset_token=" + signed_email

        # GET THE RESET TOKEN LIFETIME PARAM FROM DB
        password_reset_token_lifetime_param_instance = SystemParameter.objects.get(
            name=constants.SYSTEM_PARAM_PASSWORD_RESET_TOKEN_LIFETIME
        )

        # CAST THE VALUE OF THE PARAM TO INTEGER
        _password_reset_token_lifetime = int(
            password_reset_token_lifetime_param_instance.value
        )

        # CHECK IF THE LIFETIME IS ABLE TO CHANGED FROM SECOND UNIT TO HIGHER UNIT
        # SUCH AS DAYS, HOURS AN DMINITUES
        password_reset_token_lifetime = None
        password_reset_token_lifetime_string = ""

        one_day = 60 * 60 * 24
        one_hour = 60 * 60
        one_min = 60

        if _password_reset_token_lifetime >= one_day:
            password_reset_token_lifetime = round(
                _password_reset_token_lifetime / one_day, 1
            )
            password_reset_token_lifetime_string = (
                f"{password_reset_token_lifetime} days"
            )
        elif (
            _password_reset_token_lifetime < one_day
            and _password_reset_token_lifetime >= one_hour
        ):
            password_reset_token_lifetime = round(
                _password_reset_token_lifetime / one_hour, 1
            )
            password_reset_token_lifetime_string = (
                f"{password_reset_token_lifetime} hours"
            )
        elif (
            _password_reset_token_lifetime < one_hour
            and _password_reset_token_lifetime >= one_min
        ):
            password_reset_token_lifetime = round(
                _password_reset_token_lifetime / one_min, 1
            )
            password_reset_token_lifetime_string = (
                f"{password_reset_token_lifetime} minutes"
            )
        else:
            password_reset_token_lifetime = _password_reset_token_lifetime
            password_reset_token_lifetime_string = (
                f"{password_reset_token_lifetime} seconds"
            )

        # SAVE TOKEN TO CACHE AND SET THE TOKEN LIFE TIME  RETRIEVED FROM DB
        cache.set(user_email, signed_email, _password_reset_token_lifetime)

        # EMAIL THE RESET LINK TO THE USER
        tasks.send_password_reset_link_email.delay(
            reset_url=pass_reset_url,
            recipient=user_email,
            password_reset_token_lifetime=password_reset_token_lifetime_string,
        )

        return Response(
            get_success_response_dict(
                message="Password reset link will be sent to your email!"
            ),
            status=status.HTTP_200_OK,
        )


class PasswordResetView(APIView):
    """Password Change. The user need to be authenticated to change password"""

    serializer_class = auth_serializers.PasswordResetSerializer

    def post(self, request):
        # RESET URL TOKEN
        reset_token = request.query_params.get("reset_token")

        # LOGIN URL WHICH IS TO BE EMAILED TO THE USER AFTER PASSWORD RESET
        login_url = request.data.get("login_url")

        # GET THE USER EMAIL FROM THE TOKEN
        # THE TOKEN IS GENERATED IN THE FORM OF:
        # zemaedot3@gmail.com:1qaGbs:MrqxXKth2wz7L3AvvThAeet_PO1TmWqOgDqAF1dGVJo
        user_email = reset_token.split(":")[0]

        # GET THE TOKEN SAVED IN CACHE DURING RESET REQUEST
        cached_token = cache.get(user_email)

        # CHECK IF TOKEN IN THE CACHE AND TOKEN IN THE URL QUERY PARAM ARE EQUAL
        # RETURN INVALID TOKEN OTHERWISE
        if reset_token != cached_token:
            return Response(
                get_error_response_dict(message="Invalid token!"),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # GET THE RESET TOKEN LIFE TIME FROM DB
        password_reset_token_lifetime_param_instance = SystemParameter.objects.get(
            name=constants.SYSTEM_PARAM_PASSWORD_RESET_TOKEN_LIFETIME
        )

        # CAST LIFTIME TO INTEGER
        _password_reset_token_lifetime = int(
            password_reset_token_lifetime_param_instance.value
        )

        # GET SIGNER TO RETRIEVE THE SIGNED EMAIL
        signer = TimestampSigner()

        try:
            unsigned_email = signer.unsign(
                reset_token, max_age=_password_reset_token_lifetime
            )
        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # CHECK IF USER IS AUTHENTICATED
        if not request.user.is_authenticated:
            try:
                user = get_user_model().objects.get(email=user_email)
            except ObjectDoesNotExist:
                return Response(
                    get_error_response_dict(
                        message=f"User with email {user_email} does not exist"
                    )
                )
        else:
            user = request.user

        # DESERIALIZE THE INCOMING DATA
        serializer = auth_serializers.PasswordResetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # CHANGE THE PASSWORD
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()

        # UPDATE THE SESSION HAS TO PREVENT THE USER FROM BEING LOGGED OUT
        update_session_auth_hash(request, user)

        # login_url = request.build_absolute_uri(reverse("token_obtain_pair"))

        # SENT PASWORD CHANGE CONFIRMATION EMAIL TO THE USER
        tasks.send_password_change_confirmation_email.delay(
            login_url=login_url, recipient=user_email
        )

        return Response(
            get_success_response_dict(message="Password changed."),
            status=status.HTTP_200_OK,
        )
