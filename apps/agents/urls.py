from django.urls import path
from . import views

urlpatterns = [
    # AGENT ROUTES
    path("", views.AgentListCreateView.as_view(), name="list-create-agent"),
    path(
        "<int:pk>/",
        views.AgentRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-agent",
    ),
    # AGENT BRANCH ROUTES
    path(
        "<int:pk>/branches/",
        views.AgentBranchListCreateView.as_view(),
        name="list-create-agentbranch",
    ),
    path(
        "branches/<int:pk>/",
        views.AgentBranchRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-agentbranch",
    ),
    # AGENT ADMIN ROUTES
    path(
        "branches/<int:pk>/admins/",
        views.AgentAdminListCreateView.as_view(),
        name="list-create-agentadmin",
    ),
    path(
        "branches/admins/<int:pk>/",
        views.AgentAdminRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-agentadmin",
    ),
    # AGENT SERVICE SUBSCRIPTION ROUTES
    path(
        "<int:pk>/service-subscription/",
        views.ServiceSubscriptionListCreateView.as_view(),
        name="list-create-agent-service-subscription",
    ),
]
