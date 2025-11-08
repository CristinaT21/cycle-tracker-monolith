"""
Analytics Module - Handles predictions and insights.

This module is responsible for:
- Predicting next period dates
- Calculating cycle statistics
- Generating insights based on cycle data
- Identifying patterns in symptoms and moods

Module Boundaries:
- Publishes: Analytics events
- Consumes: Cycle data from cycles module, User data from users module
"""

default_app_config = 'modules.analytics.apps.AnalyticsConfig'
