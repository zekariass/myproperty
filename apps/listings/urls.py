from django.urls import path
from . import views

urlpatterns = [
    # CREATE LISTING
    path(
        "",
        views.ListingCreateView.as_view(),
        name="list-create-listing",
    ),
    # LIST PUBLIC LISTING
    path(
        "public/list/",
        views.PublicListingListUsingQuryParamAPIView.as_view(),
        name="public-listing-list",
    ),
    # AGENT LISTING LIST
    path(
        "agent/list/",
        views.AgentListingListUsingQuryParamAPIView.as_view(),
        name="agent-listing-list",
    ),
    # ADMIN LIST LISTING
    path(
        "admin/list/",
        views.AdminListingListUsingQuryParamAPIView.as_view(),
        name="admin-listing-list",
    ),
    # UPDATE, DELETE, RETRIEVE LISTING
    path(
        "<int:pk>/detail/",
        views.ListingDetailView.as_view(),
        name="retrieve-listing",
    ),
    path(
        "<int:pk>/update/",
        views.ListingUpdateView.as_view(),
        name="update-listing",
    ),
    path(
        "<int:pk>/delete/",
        views.ListingDestroyView.as_view(),
        name="destroy-listing",
    ),
    # LIST LISTING WITHOUT SPECIFYING AGENT/FOR ADMIN ONLY
    # path(
    #     "all/",
    #     views.ListingListUsingQuryParamAPIView.as_view(),
    #     name="list-all-listing",
    # ),
]
