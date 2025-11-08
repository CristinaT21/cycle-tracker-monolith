"""
URL routing for the Notifications module.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'notifications'

# Create separate routers to avoid URL conflicts
notification_router = DefaultRouter()
notification_router.register(r'', views.NotificationViewSet, basename='notification')

reminder_router = DefaultRouter()
reminder_router.register(r'', views.ReminderScheduleViewSet, basename='reminder')

urlpatterns = [
    # Preferences endpoints
    path('preferences/', views.get_notification_preferences, name='preferences'),
    path('preferences/update/', views.update_notification_preferences, name='update_preferences'),

    # Reminders endpoints (separate path to avoid conflict)
    path('reminders/', include(reminder_router.urls)),

    # Notification endpoints at root
    path('', include(notification_router.urls)),
]
