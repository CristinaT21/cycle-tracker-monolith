"""
Admin interface configuration for the Notifications module.
"""

from django.contrib import admin
from .models import NotificationTemplate, Notification, ReminderSchedule, NotificationPreference


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """Admin interface for NotificationTemplate model."""

    list_display = ['name', 'notification_type', 'is_active', 'created_at']
    list_filter = ['notification_type', 'is_active']
    search_fields = ['name', 'subject']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""

    list_display = [
        'user',
        'subject',
        'channel',
        'status',
        'scheduled_for',
        'is_read',
        'created_at',
    ]
    list_filter = ['status', 'channel', 'is_read', 'scheduled_for']
    search_fields = ['user__email', 'subject', 'body']
    readonly_fields = ['created_at', 'updated_at', 'sent_at', 'read_at']

    fieldsets = (
        ('User', {'fields': ('user', 'template')}),
        ('Content', {'fields': ('subject', 'body', 'channel')}),
        ('Status', {'fields': ('status', 'error_message')}),
        ('Scheduling', {'fields': ('scheduled_for', 'sent_at')}),
        ('User Interaction', {'fields': ('is_read', 'read_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ReminderSchedule)
class ReminderScheduleAdmin(admin.ModelAdmin):
    """Admin interface for ReminderSchedule model."""

    list_display = [
        'user',
        'reminder_type',
        'is_enabled',
        'days_before',
        'notification_channel',
        'created_at',
    ]
    list_filter = ['reminder_type', 'is_enabled', 'notification_channel']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """Admin interface for NotificationPreference model."""

    list_display = [
        'user',
        'email_enabled',
        'push_enabled',
        'period_reminders_enabled',
        'updated_at',
    ]
    list_filter = [
        'email_enabled',
        'push_enabled',
        'period_reminders_enabled',
        'ovulation_reminders_enabled',
    ]
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Channel Preferences', {
            'fields': ('email_enabled', 'push_enabled', 'sms_enabled', 'in_app_enabled')
        }),
        ('Notification Types', {
            'fields': (
                'period_reminders_enabled',
                'ovulation_reminders_enabled',
                'insights_enabled',
                'health_tips_enabled',
            )
        }),
        ('Quiet Hours', {
            'fields': ('quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
