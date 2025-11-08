"""
Admin interface configuration for the Analytics module.
"""

from django.contrib import admin
from .models import CyclePrediction, CycleStatistics, Insight


@admin.register(CyclePrediction)
class CyclePredictionAdmin(admin.ModelAdmin):
    """Admin interface for CyclePrediction model."""

    list_display = [
        'user',
        'predicted_period_start',
        'confidence_score',
        'is_active',
        'actual_period_started',
        'created_at',
    ]
    list_filter = ['is_active', 'algorithm_used', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Predictions', {
            'fields': (
                'predicted_period_start',
                'predicted_period_end',
                'predicted_ovulation_date',
                'predicted_fertile_window_start',
                'predicted_fertile_window_end',
            )
        }),
        ('Metadata', {
            'fields': (
                'confidence_score',
                'algorithm_used',
                'based_on_cycles_count',
            )
        }),
        ('Status', {
            'fields': ('is_active', 'actual_period_started')
        }),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(CycleStatistics)
class CycleStatisticsAdmin(admin.ModelAdmin):
    """Admin interface for CycleStatistics model."""

    list_display = [
        'user',
        'average_cycle_length',
        'cycle_regularity_score',
        'total_cycles_tracked',
        'last_calculated',
    ]
    search_fields = ['user__email']
    readonly_fields = ['last_calculated', 'created_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Cycle Statistics', {
            'fields': (
                'average_cycle_length',
                'shortest_cycle_length',
                'longest_cycle_length',
                'cycle_regularity_score',
            )
        }),
        ('Period Statistics', {
            'fields': (
                'average_period_length',
                'shortest_period_length',
                'longest_period_length',
            )
        }),
        ('Data Quality', {
            'fields': ('total_cycles_tracked', 'complete_cycles_count')
        }),
        ('Timestamps', {'fields': ('last_calculated', 'created_at')}),
    )


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    """Admin interface for Insight model."""

    list_display = [
        'user',
        'title',
        'category',
        'priority',
        'is_read',
        'is_dismissed',
        'created_at',
    ]
    list_filter = ['category', 'priority', 'is_read', 'is_dismissed', 'created_at']
    search_fields = ['user__email', 'title', 'description']
    readonly_fields = ['created_at', 'read_at']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Insight Details', {
            'fields': ('category', 'priority', 'title', 'description')
        }),
        ('Status', {
            'fields': ('is_read', 'is_dismissed', 'read_at')
        }),
        ('Metadata', {
            'fields': ('generated_by', 'based_on_data_until')
        }),
        ('Timestamps', {'fields': ('created_at',)}),
    )
