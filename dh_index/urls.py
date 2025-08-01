"""
URL configuration for dh_index project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.routers import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.routers'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi

from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Đại Hiệp - Index Django API",
        default_version='v1', ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include("dh_index.apps.urls_api"), name='admin_home'),
  path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static("media", document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                              document_root=settings.STATIC_ROOT)
