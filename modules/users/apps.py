"""
Users module application configuration.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for the Users module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.users'
    verbose_name = 'User Management & Authentication'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        # Import signals here to avoid circular imports
        # import modules.users.signals
        pass
