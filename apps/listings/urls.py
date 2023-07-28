from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.ListingListCreateView.as_view(),
        name="list-create-listing",
    ),
    # UPDATE, DELETE, RETRIEVE LISTING
    path(
        "<int:pk>/",
        views.RetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy-listing",
    ),
    # LIST LISTING WITHOUT SPECIFYING AGENT/FOR ADMIN ONLY
    path(
        "all/",
        views.ListingListUsingQuryParamAPIView.as_view(),
        name="list-all-listing",
    ),
]
