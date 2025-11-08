"""
Cycles Module - Handles menstrual cycle tracking.

This module is responsible for:
- Recording period start and end dates
- Tracking symptoms and moods
- Recording flow intensity
- Managing cycle history

Module Boundaries:
- Publishes: Cycle update events (for analytics and notifications)
- Consumes: User data from users module
"""

default_app_config = 'modules.cycles.apps.CyclesConfig'
