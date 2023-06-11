from turtle import title
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

from rest_framework_simplejwt.views import (TokenObtainPairView, 
                                            TokenRefreshView)
from rest_framework import urls as rest_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("myproperty-schema/", get_schema_view(
        title="Myproperty Schema",
        description="API reference of Myproperty backend",
        version="1.0.0",
        public=True
         ), name="myproperty-schema",
         
    ),
    path("myproperty-api-docmentation/", TemplateView.as_view(
        template_name="docmentation/myproperty-doc.html",
        extra_context={"schema_url": "myproperty-schema"}
        
    ), name="myproperty-api-docmentation"),

    # SimpleJWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api-auth/", include(rest_urls)),

    # User module
    path("users/", include("apps.users.urls")),

    # System module
    path("system/", include("apps.system.urls")),

    # Commons module
    path("commons/", include("apps.commons.urls")),


    # Agents module
    path("agents/", include("apps.agents.urls")),
]
