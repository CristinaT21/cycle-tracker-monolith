"""
Analytics module application configuration.
"""

from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """Configuration for the Analytics module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.analytics'
    verbose_name = 'Analytics & Predictions'

    def ready(self):
        """Import signal handlers when the app is ready."""
        pass
