from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from apps.mixins.permissions import IsAgent
from apps.agents import models as agent_models

from . import models as notif_models
from . import serializers as notif_serializers


class UserNotificationPreferenceListCreateView(ListCreateAPIView):
    queryset = notif_models.UserNotificationPreference.objects.all()
    serializer_class = notif_serializers.UserNotificationPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]

    def post(self, request):
        try:
            # GET THE USER FROM REQUEST
            user = request.user
            if user:
                pref_serializer = self.get_serializer(data=request.data)
                pref_serializer.is_valid(raise_exception=True)
                pref_serializer.save(user=user)
                return Response(
                    {"details": pref_serializer.data}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"errors": "Anonymous user cannot create preference. Signup first."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserNotificationPreferenceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = notif_models.UserNotificationPreference.objects.all()
    serializer_class = notif_serializers.UserNotificationPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]


class UserNotificationChannelPreferenceListCreateView(ListCreateAPIView):
    queryset = notif_models.UserNotificationChannelPreference.objects.all()
    serializer_class = notif_serializers.UserNotificationChannelPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]

    def post(self, request):
        try:
            # GET THE USER FROM REQUEST
            user = request.user
            if user:
                pref_serializer = self.get_serializer(data=request.data)
                pref_serializer.is_valid(raise_exception=True)
                pref_serializer.save(user=user)
                return Response(
                    {"details": pref_serializer.data}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"errors": "Anonymous user cannot create preference. Signup first."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_404_NOT_FOUND)


class UserNotificationChannelPreferenceRetrieveUpdateDestroyView(
    RetrieveUpdateDestroyAPIView
):
    queryset = notif_models.UserNotificationChannelPreference.objects.all()
    serializer_class = notif_serializers.UserNotificationChannelPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]


class AgentNotificationPreferenceListCreateView(ListCreateAPIView):
    queryset = notif_models.AgentNotificationPreference.objects.all()
    serializer_class = notif_serializers.AgentNotificationPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]

    def post(self, request, *args, **kwargs):
        try:
            agent_id = kwargs["agent_id"]

            try:
                agent_instance = agent_models.Agent.objects.get(id=agent_id)
            except:
                return Response(
                    {"errors": f"Agent with id{agent_id} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if agent_instance:
                pref_serializer = self.get_serializer(data=request.data)
                pref_serializer.is_valid(raise_exception=True)
                pref_serializer.save(agent=agent_instance)
                return Response(
                    {"details": pref_serializer.data}, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "errors": "Anonymous agent cannot create preference. Crate Agent first."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_404_NOT_FOUND)


class AgentNotificationPreferenceRetrieveUpdateDestroyView(
    RetrieveUpdateDestroyAPIView
):
    queryset = notif_models.AgentNotificationPreference.objects.all()
    serializer_class = notif_serializers.AgentNotificationPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]


class AgentNotificationChannelPreferenceListCreateView(ListCreateAPIView):
    queryset = notif_models.AgentNotificationChannelPreference.objects.all()
    serializer_class = notif_serializers.AgentNotificationChannelPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]

    def post(self, request, *args, **kwargs):
        try:
            agent_id = kwargs["agent_id"]
            try:
                agent_instance = agent_models.Agent.objects.get(id=agent_id)
            except:
                return Response(
                    {"errors": f"Agent with id{agent_id} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if agent_instance:
                pref_serializer = self.get_serializer(data=request.data)
                pref_serializer.is_valid(raise_exception=True)
                pref_serializer.save(agent=agent_instance)
                return Response(
                    {"details": pref_serializer.data}, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "errors": "Anonymous agent cannot create preference. Create Agent first."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_404_NOT_FOUND)


class AgentNotificationChannelPreferenceRetrieveUpdateDestroyView(
    RetrieveUpdateDestroyAPIView
):
    queryset = notif_models.AgentNotificationChannelPreference.objects.all()
    serializer_class = notif_serializers.AgentNotificationChannelPreferenceSerializer
    permission_classes = [IsAdminUser, IsAgent]
