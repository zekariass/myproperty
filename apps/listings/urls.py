from django.urls import path
from . import views

urlpatterns = [
    # CREATE LISTING
    path(
        "create/agent/",
        views.ListingCreateView.as_view(),
        name="list-create-listing",
    ),
    # LIST PUBLIC LISTING
    path(
        "list/public/",
        views.PublicListingListUsingQuryParamAPIView.as_view(),
        name="public-listing-list",
    ),
    # AGENT LISTING LIST
    path(
        "list/agent/",
        views.AgentListingListUsingQuryParamAPIView.as_view(),
        name="agent-listing-list",
    ),
    # ADMIN LIST LISTING
    path(
        "list/admin/",
        views.AdminListingListUsingQuryParamAPIView.as_view(),
        name="admin-listing-list",
    ),
    # UPDATE, DELETE, RETRIEVE LISTING
    path(
        "<int:pk>/detail/agent/",
        views.ListingDetailView.as_view(),
        name="agent-retrieve-listing",
    ),
    path(
        "<int:pk>/update/agent/",
        views.ListingUpdateView.as_view(),
        name="agent-update-listing",
    ),
    path(
        "<int:pk>/delete/agent/",
        views.ListingDestroyView.as_view(),
        name="agent-destroy-listing",
    ),
    # LIST LISTING WITHOUT SPECIFYING AGENT/FOR ADMIN ONLY
    # path(
    #     "all/",
    #     views.ListingListUsingQuryParamAPIView.as_view(),
    #     name="list-all-listing",
    # ),
]
