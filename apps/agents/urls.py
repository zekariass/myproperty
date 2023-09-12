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
    # GET AGENT PAY_PER_LISTING DISCOUNTS
    path(
        "<int:pk>/ppl-discounts/",
        views.GetPayPerListingDiscountView.as_view(),
        name="get-agent-pay-per-listing-discount",
    ),
    # GET AGENT SUBSCRIPTION DISCOUNTS
    path(
        "<int:pk>/subscription-discounts/",
        views.GetSubscriptionDiscountView.as_view(),
        name="get-agent-subscription-discount",
    ),
    # CREATE LIST REQUEST
    path(
        "client-requests/",
        views.RequestListCreateView.as_view(),
        name="create-client-request",
    ),
    # RETRIEVE REQUEST
    path(
        "requests/<int:pk>/",
        views.RequestRetrieveView.as_view(),
        name="retrieve-request",
    ),
    # GET AGENT REQUESTS
    path(
        "requests/",  # ?agent=1
        views.RequestRetrieveByAgentView.as_view(),
        name="list-request-by-agent",
    ),
]
