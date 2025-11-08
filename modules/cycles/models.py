"""
Models for cycle tracking.
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Cycle(models.Model):
    """
    Represents a single menstrual cycle.

    A cycle starts on the first day of menstruation and ends
    the day before the next menstruation starts.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cycles')
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, blank=True, db_index=True)

    # Cycle metrics
    cycle_length = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(21), MaxValueValidator(45)]
    )
    period_length = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2), MaxValueValidator(10)]
    )

    # Status
    is_active = models.BooleanField(default=True)  # True if this is the current cycle
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cycles'
        verbose_name = 'Cycle'
        verbose_name_plural = 'Cycles'
        ordering = ['-start_date']
        unique_together = ['user', 'start_date']
        indexes = [
            models.Index(fields=['user', '-start_date']),
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"Cycle for {self.user.email} starting {self.start_date}"

    def calculate_cycle_length(self):
        """Calculate and update the cycle length if end date is set."""
        if self.end_date:
            self.cycle_length = (self.end_date - self.start_date).days + 1
            return self.cycle_length
        return None


class PeriodDay(models.Model):
    """
    Represents a single day of menstruation within a cycle.
    """

    FLOW_CHOICES = [
        ('spotting', 'Spotting'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ]

    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='period_days')
    date = models.DateField(db_index=True)
    flow = models.CharField(max_length=20, choices=FLOW_CHOICES)
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'period_days'
        verbose_name = 'Period Day'
        verbose_name_plural = 'Period Days'
        ordering = ['date']
        unique_together = ['cycle', 'date']
        indexes = [
            models.Index(fields=['cycle', 'date']),
        ]

    def __str__(self):
        return f"Period day {self.date} - {self.flow}"


class Symptom(models.Model):
    """
    Predefined symptoms that users can track.
    """

    CATEGORY_CHOICES = [
        ('physical', 'Physical'),
        ('emotional', 'Emotional'),
        ('digestive', 'Digestive'),
        ('skin', 'Skin'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'symptoms'
        verbose_name = 'Symptom'
        verbose_name_plural = 'Symptoms'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class DailyLog(models.Model):
    """
    Daily log for tracking symptoms, moods, and other data.

    Can be associated with a cycle or standalone.
    """

    MOOD_CHOICES = [
        ('great', 'Great'),
        ('good', 'Good'),
        ('okay', 'Okay'),
        ('bad', 'Bad'),
        ('terrible', 'Terrible'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_logs')
    cycle = models.ForeignKey(Cycle, on_delete=models.SET_NULL, null=True, blank=True, related_name='daily_logs')
    date = models.DateField(db_index=True)

    # Mood tracking
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, null=True, blank=True)

    # Symptoms
    symptoms = models.ManyToManyField(Symptom, blank=True, related_name='daily_logs')

    # Additional tracking
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sexual_activity = models.BooleanField(default=False)

    # Notes
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_logs'
        verbose_name = 'Daily Log'
        verbose_name_plural = 'Daily Logs'
        ordering = ['-date']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['cycle', 'date']),
        ]

    def __str__(self):
        return f"Log for {self.user.email} on {self.date}"
