from turtle import title
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "myproperty-schema/",
        get_schema_view(
            title="Myproperty Schema",
            description="API reference of Myproperty backend",
            version="1.0.0",
            public=True,
        ),
        name="myproperty-schema",
    ),
    path(
        "api-documentation/",
        TemplateView.as_view(
            template_name="docmentation/myproperty-doc.html",
            extra_context={"schema_url": "myproperty-schema"},
        ),
        name="api-documentation",
    ),
    # User module
    path("users/", include("apps.users.urls")),
    # System module
    path("system/", include("apps.system.urls")),
    # Commons module
    path("commons/", include("apps.commons.urls")),
    # Agents module
    path("agents/", include("apps.agents.urls")),
    # Property module
    path("properties/", include("apps.properties.urls")),
    # Listing module
    path("listings/", include("apps.listings.urls")),
    # Payment module
    path("payments/", include("apps.payments.urls")),
    # Notification module
    path("notifications/", include("apps.notifications.urls")),
]
