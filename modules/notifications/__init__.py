"""
Notifications Module - Handles reminders and notifications.

This module is responsible for:
- Managing notification preferences
- Scheduling period reminders
- Sending notifications (email, push, etc.)
- Tracking notification history

Module Boundaries:
- Publishes: None
- Consumes: User data, Cycle data, Prediction data
"""

default_app_config = 'modules.notifications.apps.NotificationsConfig'
