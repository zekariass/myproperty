from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCreatePaymentView.as_view(), name="list-create-payment"),
    path(
        "<int:pk>/approve/", views.ApprovePaymentView.as_view(), name="approve-payment"
    ),
    path(
        "unapproved-payments/",
        views.UnapprovedPaymentListView.as_view(),
        name="list-unapproved-payments",
    ),
    path(
        "approved-payments/",
        views.ApprovedPaymentListView.as_view(),
        name="list-approved-payments",
    ),
]
