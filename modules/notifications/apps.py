"""
Notifications module application configuration.
"""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Configuration for the Notifications module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.notifications'
    verbose_name = 'Notifications & Reminders'

    def ready(self):
        """Import signal handlers when the app is ready."""
        pass
