"""
URL routing for the Notifications module.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'notifications'

router = DefaultRouter()
router.register(r'', views.NotificationViewSet, basename='notification')
router.register(r'reminders', views.ReminderScheduleViewSet, basename='reminder')

urlpatterns = [
    # Preferences endpoints
    path('preferences/', views.get_notification_preferences, name='preferences'),
    path('preferences/update/', views.update_notification_preferences, name='update_preferences'),

    # Router URLs
    path('', include(router.urls)),
]
