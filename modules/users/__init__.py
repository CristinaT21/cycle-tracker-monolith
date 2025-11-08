"""
Users Module - Handles authentication and user management.

This module is responsible for:
- User registration and authentication
- User profile management
- JWT token management
- User preferences and settings

Module Boundaries:
- Publishes: User authentication events
- Consumes: None (independent module)
"""

default_app_config = 'modules.users.apps.UsersConfig'
