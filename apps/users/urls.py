from django.urls import path
from . import views as auth_views

urlpatterns = [
    # Users
    path("", auth_views.UserCreateView.as_view(), name = "list-create-users"),
    path("list/", auth_views.UserListView.as_view(), name = "list-list-users"),
    path("change-password/", auth_views.ChangeUserPasswordView.as_view(), name = "change-password"),
    path("<int:pk>/", auth_views.UserRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-user"),
    # path("<int:pk>/update", auth_views.UserRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-user"),
    
    # User Groups
    path("groups/", auth_views.GroupListCreateView.as_view(), name = "list-create-groups"),
    path("group/<int:pk>/", auth_views.GroupRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-group"),

    # Roles
    path("roles/", auth_views.RoleListCreateView.as_view(), name = "list-create-roles"),
    path("role/<int:pk>/", auth_views.RoleRetrieveUpdateDestroyView.as_view(), name = "retrieve-update-destroy-role"),
]
