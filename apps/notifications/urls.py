from django.urls import path

from . import views

urlpatterns = [
    # USER NOTIFICATION PREFERENCE
    path(
        "user/preferences/",
        views.UserNotificationPreferenceListCreateView.as_view(),
        name="list-create-usernotificationpreference",
    ),
    path(
        "user/preferences/<int:pk>/",
        views.UserNotificationPreferenceRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-usernotificationpreference",
    ),
    # USER NOTIFICATION CHANNEL PREFERENCE
    path(
        "user/channel-preferences/",
        views.UserNotificationChannelPreferenceListCreateView.as_view(),
        name="list-create-usernotificationchannelpreference",
    ),
    path(
        "user/channel-preferences/<int:pk>/",
        views.UserNotificationChannelPreferenceRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-usernotificationchannelpreference",
    ),
    # AGENT NOTIFICATION PREFERENCE
    path(
        "agent/<int:agent_id>/preferences/",
        views.AgentNotificationPreferenceListCreateView.as_view(),
        name="list-create-agentnotificationpreference",
    ),
    path(
        "agent/preferences/<int:pk>/",
        views.AgentNotificationPreferenceRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-agentnotificationpreference",
    ),
    # AGENT NOTIFICATION CHANNEL PREFERENCE
    path(
        "agent/<int:agent_id>/channel-preferences/",
        views.AgentNotificationChannelPreferenceListCreateView.as_view(),
        name="list-create-agentnotificationchannelpreference",
    ),
    path(
        "agent/channel-preferences/<int:pk>/",
        views.AgentNotificationChannelPreferenceRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-agentnotificationchannelpreference",
    ),
]
