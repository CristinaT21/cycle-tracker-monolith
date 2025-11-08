"""
Serializers for the Analytics module.
"""

from rest_framework import serializers
from .models import CyclePrediction, CycleStatistics, Insight


class CyclePredictionSerializer(serializers.ModelSerializer):
    """Serializer for cycle predictions."""

    class Meta:
        model = CyclePrediction
        fields = [
            'id',
            'predicted_period_start',
            'predicted_period_end',
            'predicted_ovulation_date',
            'predicted_fertile_window_start',
            'predicted_fertile_window_end',
            'confidence_score',
            'algorithm_used',
            'based_on_cycles_count',
            'is_active',
            'created_at',
        ]
        read_only_fields = fields


class CycleStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for cycle statistics."""

    class Meta:
        model = CycleStatistics
        fields = [
            'average_cycle_length',
            'shortest_cycle_length',
            'longest_cycle_length',
            'cycle_regularity_score',
            'average_period_length',
            'shortest_period_length',
            'longest_period_length',
            'total_cycles_tracked',
            'complete_cycles_count',
            'last_calculated',
        ]
        read_only_fields = fields


class InsightSerializer(serializers.ModelSerializer):
    """Serializer for insights."""

    class Meta:
        model = Insight
        fields = [
            'id',
            'category',
            'priority',
            'title',
            'description',
            'is_read',
            'is_dismissed',
            'created_at',
            'read_at',
        ]
        read_only_fields = ['id', 'category', 'priority', 'title', 'description', 'created_at']


class InsightUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating insight status."""

    class Meta:
        model = Insight
        fields = ['is_read', 'is_dismissed']
