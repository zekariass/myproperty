from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCreatePaymentView.as_view(), name="list-create-payment"),
]
