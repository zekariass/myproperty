from django.urls import path, include
from . import views as auth_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import urls as rest_urls

urlpatterns = [
    # SimpleJWT Auth
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include(rest_urls)),
    # Users
    path("", auth_views.UserCreateView.as_view(), name="create-users"),
    path("list/", auth_views.UserListView.as_view(), name="list-users"),
    # path(
    #     "change-password/",
    #     auth_views.ChangeUserPasswordView.as_view(),
    #     name="change-password",
    # ),
    path(
        "password/reset/request/",
        auth_views.PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(),
        name="user-password-reset",
    ),
    path(
        "<int:pk>/",
        auth_views.UserRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-user",
    ),
    # User Groups
    path(
        "groups/", auth_views.GroupListCreateView.as_view(), name="list-create-groups"
    ),
    path(
        "group/<int:pk>/",
        auth_views.GroupRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-group",
    ),
    # Roles
    path("roles/", auth_views.RoleListCreateView.as_view(), name="list-create-roles"),
    path(
        "role/<int:pk>/",
        auth_views.RoleRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-role",
    ),
]
