"""
Models for notifications and reminders.
"""

from django.db import models
from django.conf import settings


class NotificationTemplate(models.Model):
    """
    Templates for different types of notifications.
    """

    TYPE_CHOICES = [
        ('period_reminder', 'Period Reminder'),
        ('ovulation_reminder', 'Ovulation Reminder'),
        ('cycle_insights', 'Cycle Insights'),
        ('health_tip', 'Health Tip'),
        ('custom', 'Custom'),
    ]

    name = models.CharField(max_length=100, unique=True)
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    body_template = models.TextField(help_text="Use {variable_name} for dynamic content")
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_templates'
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'

    def __str__(self):
        return f"{self.name} ({self.notification_type})"


class Notification(models.Model):
    """
    Individual notification instances sent to users.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('sms', 'SMS'),
        ('in_app', 'In-App'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )

    # Notification content
    subject = models.CharField(max_length=200)
    body = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)

    # Scheduling
    scheduled_for = models.DateTimeField(db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    # User interaction
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-scheduled_for']
        indexes = [
            models.Index(fields=['user', '-scheduled_for']),
            models.Index(fields=['status', 'scheduled_for']),
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.subject} to {self.user.email}"


class ReminderSchedule(models.Model):
    """
    Recurring reminder schedules for users.
    """

    REMINDER_TYPE_CHOICES = [
        ('period', 'Period Reminder'),
        ('ovulation', 'Ovulation Reminder'),
        ('daily_log', 'Daily Log Reminder'),
        ('custom', 'Custom'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reminder_schedules'
    )

    # Reminder configuration
    reminder_type = models.CharField(max_length=30, choices=REMINDER_TYPE_CHOICES)
    is_enabled = models.BooleanField(default=True)
    days_before = models.IntegerField(default=2, help_text="Days before event to send reminder")

    # Notification preferences
    notification_channel = models.CharField(max_length=20, default='in_app')
    notification_time = models.TimeField(default='09:00:00', help_text="Time of day to send reminder")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reminder_schedules'
        verbose_name = 'Reminder Schedule'
        verbose_name_plural = 'Reminder Schedules'
        unique_together = ['user', 'reminder_type']

    def __str__(self):
        return f"{self.reminder_type} reminder for {self.user.email}"


class NotificationPreference(models.Model):
    """
    User preferences for notifications.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )

    # Channel preferences
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=False)
    sms_enabled = models.BooleanField(default=False)
    in_app_enabled = models.BooleanField(default=True)

    # Notification types
    period_reminders_enabled = models.BooleanField(default=True)
    ovulation_reminders_enabled = models.BooleanField(default=False)
    insights_enabled = models.BooleanField(default=True)
    health_tips_enabled = models.BooleanField(default=True)

    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'

    def __str__(self):
        return f"Notification preferences for {self.user.email}"
