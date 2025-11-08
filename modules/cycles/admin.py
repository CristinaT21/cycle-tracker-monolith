"""
Admin interface configuration for the Cycles module.
"""

from django.contrib import admin
from .models import Cycle, PeriodDay, Symptom, DailyLog


class PeriodDayInline(admin.TabularInline):
    """Inline admin for period days within a cycle."""

    model = PeriodDay
    extra = 0
    fields = ['date', 'flow', 'notes']


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    """Admin interface for Cycle model."""

    list_display = [
        'user',
        'start_date',
        'end_date',
        'cycle_length',
        'period_length',
        'is_active',
        'created_at',
    ]
    list_filter = ['is_active', 'start_date', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['cycle_length', 'created_at', 'updated_at']
    inlines = [PeriodDayInline]

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Cycle Dates', {'fields': ('start_date', 'end_date', 'cycle_length', 'period_length')}),
        ('Status', {'fields': ('is_active', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PeriodDay)
class PeriodDayAdmin(admin.ModelAdmin):
    """Admin interface for PeriodDay model."""

    list_display = ['cycle', 'date', 'flow', 'created_at']
    list_filter = ['flow', 'date']
    search_fields = ['cycle__user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    """Admin interface for Symptom model."""

    list_display = ['name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    """Admin interface for DailyLog model."""

    list_display = ['user', 'date', 'mood', 'temperature', 'created_at']
    list_filter = ['mood', 'date', 'sexual_activity']
    search_fields = ['user__email', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['symptoms']

    fieldsets = (
        ('User & Date', {'fields': ('user', 'cycle', 'date')}),
        ('Tracking', {
            'fields': ('mood', 'symptoms', 'temperature', 'weight', 'sexual_activity')
        }),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
