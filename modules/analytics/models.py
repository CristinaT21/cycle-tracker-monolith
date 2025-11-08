"""
Models for analytics and predictions.
"""

from django.db import models
from django.conf import settings


class CyclePrediction(models.Model):
    """
    Stores predictions for upcoming cycles.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')

    # Predicted dates
    predicted_period_start = models.DateField(db_index=True)
    predicted_period_end = models.DateField()
    predicted_ovulation_date = models.DateField(null=True, blank=True)
    predicted_fertile_window_start = models.DateField(null=True, blank=True)
    predicted_fertile_window_end = models.DateField(null=True, blank=True)

    # Prediction metadata
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    algorithm_used = models.CharField(max_length=50, default='average')
    based_on_cycles_count = models.IntegerField(default=0)

    # Status
    is_active = models.BooleanField(default=True)
    actual_period_started = models.DateField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cycle_predictions'
        verbose_name = 'Cycle Prediction'
        verbose_name_plural = 'Cycle Predictions'
        ordering = ['-predicted_period_start']
        indexes = [
            models.Index(fields=['user', '-predicted_period_start']),
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"Prediction for {self.user.email} - {self.predicted_period_start}"


class CycleStatistics(models.Model):
    """
    Aggregated statistics about a user's cycles.

    Recalculated periodically or when cycles are updated.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cycle_statistics'
    )

    # Cycle statistics
    average_cycle_length = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    shortest_cycle_length = models.IntegerField(default=0)
    longest_cycle_length = models.IntegerField(default=0)
    cycle_regularity_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Period statistics
    average_period_length = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    shortest_period_length = models.IntegerField(default=0)
    longest_period_length = models.IntegerField(default=0)

    # Data quality
    total_cycles_tracked = models.IntegerField(default=0)
    complete_cycles_count = models.IntegerField(default=0)

    # Timestamps
    last_calculated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cycle_statistics'
        verbose_name = 'Cycle Statistics'
        verbose_name_plural = 'Cycle Statistics'

    def __str__(self):
        return f"Statistics for {self.user.email}"


class Insight(models.Model):
    """
    Generated insights and recommendations for users.
    """

    CATEGORY_CHOICES = [
        ('cycle', 'Cycle Pattern'),
        ('symptom', 'Symptom Pattern'),
        ('mood', 'Mood Pattern'),
        ('health', 'Health Recommendation'),
        ('general', 'General'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='insights')

    # Insight details
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Status
    is_read = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)

    # Metadata
    generated_by = models.CharField(max_length=100, default='system')
    based_on_data_until = models.DateField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'insights'
        verbose_name = 'Insight'
        verbose_name_plural = 'Insights'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.title} for {self.user.email}"
