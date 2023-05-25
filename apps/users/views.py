
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password

from rest_framework.generics import (RetrieveUpdateDestroyAPIView, 
                                     RetrieveDestroyAPIView,
                                     ListCreateAPIView, 
                                     UpdateAPIView,
                                     CreateAPIView,
                                     ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators  import schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from . import serializers as auth_serializers
from . import models as auth_models

#=============Roles==============================================================
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



#=============Groups==============================================================
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


#=============Users==============================================================

class UserCreateView(CreateAPIView):
    """Create User View. This view does not need the user to be authenicated to create user"""
    queryset = get_user_model().objects.all()
    serializer_class = auth_serializers.MypropertyUserSerializer


class UserListView(ListAPIView):
    """List users of the system. This view checks if the user is Admin. Oly admin users can
    see list of users"""
    queryset = get_user_model().objects.all()
    serializer_class = auth_serializers.MypropertyUserSerializer
    permission_classes = (IsAdminUser)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """This view is used to retrieve, delete and update a user. User need to be authenticated 
    to be able to do these operations."""
    queryset = get_user_model().objects.all()
    serializer_class = auth_serializers.MypropertyUserNoPasswordSerializer
    permission_classes = (IsAuthenticated,)


class ChangeUserPasswordView(UpdateAPIView):
    """Password Change. The user need to be authenticated to change password"""
    serializer_class = auth_serializers.ChangeUserPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        #Check old password
        if not user.check_password(serializer.data.get("old_password")):
            return Response(data = "Wrong old password!", status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.data.get("new_password") != serializer.data.get("confirm_password"):
            return Response(data = "New password do not match!", status=status.HTTP_400_BAD_REQUEST)
            
        #Change password
        user.set_password(serializer.data.get("new_password"))
        user.save()

        #Update the session has to prevent the user from being logged out
        update_session_auth_hash(request, user)

        return Response(data = "Password Changed!", status=status.HTTP_200_OK)
