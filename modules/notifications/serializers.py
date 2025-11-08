"""
Serializers for the Notifications module.
"""

from rest_framework import serializers
from .models import Notification, ReminderSchedule, NotificationPreference, NotificationTemplate


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer for notification templates."""

    class Meta:
        model = NotificationTemplate
        fields = ['id', 'name', 'notification_type', 'subject', 'is_active']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""

    template_name = serializers.CharField(source='template.name', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'subject',
            'body',
            'channel',
            'status',
            'scheduled_for',
            'sent_at',
            'is_read',
            'read_at',
            'template_name',
            'created_at',
        ]
        read_only_fields = fields


class ReminderScheduleSerializer(serializers.ModelSerializer):
    """Serializer for reminder schedules."""

    class Meta:
        model = ReminderSchedule
        fields = [
            'id',
            'reminder_type',
            'is_enabled',
            'days_before',
            'notification_channel',
            'notification_time',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for notification preferences."""

    class Meta:
        model = NotificationPreference
        fields = [
            'email_enabled',
            'push_enabled',
            'sms_enabled',
            'in_app_enabled',
            'period_reminders_enabled',
            'ovulation_reminders_enabled',
            'insights_enabled',
            'health_tips_enabled',
            'quiet_hours_enabled',
            'quiet_hours_start',
            'quiet_hours_end',
            'updated_at',
        ]
        read_only_fields = ['updated_at']
