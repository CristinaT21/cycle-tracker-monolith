"""
URL Configuration for Cycle Tracker Modular Monolith.

This file routes requests to appropriate modules while maintaining
clear boundaries between business domains.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Module routes - each module exposes its own API endpoints
    # Following RESTful conventions and modular boundaries
    path('api/v1/auth/', include('modules.users.urls')),
    path('api/v1/cycles/', include('modules.cycles.urls')),
    path('api/v1/analytics/', include('modules.analytics.urls')),
    path('api/v1/notifications/', include('modules.notifications.urls')),
    path('api/v1/visualizations/', include('modules.visualizations.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
