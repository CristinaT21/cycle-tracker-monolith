"""
Cycles module application configuration.
"""

from django.apps import AppConfig


class CyclesConfig(AppConfig):
    """Configuration for the Cycles module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.cycles'
    verbose_name = 'Cycle Tracking'

    def ready(self):
        """Import signal handlers when the app is ready."""
        # import modules.cycles.signals
        pass
