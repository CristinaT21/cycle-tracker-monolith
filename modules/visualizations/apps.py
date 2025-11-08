"""
Visualizations module application configuration.
"""

from django.apps import AppConfig


class VisualizationsConfig(AppConfig):
    """Configuration for the Visualizations module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.visualizations'
    verbose_name = 'Data Visualization'

    def ready(self):
        """Import signal handlers when the app is ready."""
        pass
