"""
Serializers for the Cycles module.
"""

from rest_framework import serializers
from .models import Cycle, PeriodDay, Symptom, DailyLog
from shared.exceptions import ValidationException


class SymptomSerializer(serializers.ModelSerializer):
    """Serializer for Symptom model."""

    class Meta:
        model = Symptom
        fields = ['id', 'name', 'category', 'description']


class PeriodDaySerializer(serializers.ModelSerializer):
    """Serializer for PeriodDay model."""

    class Meta:
        model = PeriodDay
        fields = ['id', 'date', 'flow', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CycleSerializer(serializers.ModelSerializer):
    """Serializer for Cycle model."""

    period_days = PeriodDaySerializer(many=True, read_only=True)

    class Meta:
        model = Cycle
        fields = [
            'id',
            'start_date',
            'end_date',
            'cycle_length',
            'period_length',
            'is_active',
            'notes',
            'period_days',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'cycle_length', 'period_length', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate cycle dates."""
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if end_date and start_date and end_date < start_date:
            raise ValidationException("End date must be after start date")

        return attrs


class CycleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new cycle."""

    class Meta:
        model = Cycle
        fields = ['start_date', 'notes']

    def create(self, validated_data):
        """Create a new cycle and mark previous cycles as inactive."""
        user = self.context['request'].user

        # Mark all previous cycles as inactive
        Cycle.objects.filter(user=user, is_active=True).update(is_active=False)

        # Create new active cycle
        cycle = Cycle.objects.create(user=user, is_active=True, **validated_data)
        return cycle


class DailyLogSerializer(serializers.ModelSerializer):
    """Serializer for DailyLog model."""

    symptoms = SymptomSerializer(many=True, read_only=True)
    symptom_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = DailyLog
        fields = [
            'id',
            'date',
            'mood',
            'symptoms',
            'symptom_ids',
            'temperature',
            'weight',
            'sexual_activity',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'symptoms', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create daily log with symptoms."""
        symptom_ids = validated_data.pop('symptom_ids', [])
        user = self.context['request'].user

        daily_log = DailyLog.objects.create(user=user, **validated_data)

        if symptom_ids:
            daily_log.symptoms.set(symptom_ids)

        return daily_log

    def update(self, instance, validated_data):
        """Update daily log with symptoms."""
        symptom_ids = validated_data.pop('symptom_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if symptom_ids is not None:
            instance.symptoms.set(symptom_ids)

        return instance
