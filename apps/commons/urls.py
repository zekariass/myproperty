from django.urls import path

from . import views

urlpatterns = [
    # COUNTRY ROUTES
    path(
        "countries/", views.CountryListCreateView.as_view(), name="list-create-country"
    ),
    path(
        "countries/<int:pk>/",
        views.CountryRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-country",
    ),
    # ADDRESS ROUTES
    path(
        "addresses/", views.AddressListCreateView.as_view(), name="list-create-address"
    ),
    path(
        "addresses/<int:pk>/",
        views.AddressRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-address",
    ),
    # TAG ROUTES
    path("tags/", views.TagListCreateView.as_view(), name="list-create-tag"),
    path(
        "tags/<int:pk>/",
        views.TagRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-tag",
    ),
]
