"""
Business logic services for analytics and predictions.
"""

from datetime import timedelta
from decimal import Decimal
from typing import Optional, Dict, Any
from django.conf import settings
from django.utils import timezone

from modules.cycles.models import Cycle, DailyLog
from .models import CyclePrediction, CycleStatistics, Insight


class PredictionService:
    """
    Service for generating cycle predictions.
    """

    def __init__(self, user):
        self.user = user
        self.min_cycles = settings.ANALYTICS_CONFIG.get('MIN_CYCLES_FOR_PREDICTION', 3)

    def generate_prediction(self) -> Optional[CyclePrediction]:
        """
        Generate a new prediction for the user's next cycle.

        Returns:
            CyclePrediction object or None if insufficient data
        """
        # Get all cycles ordered by start date (oldest to newest)
        all_cycles = list(Cycle.objects.filter(
            user=self.user
        ).order_by('start_date'))

        if len(all_cycles) < self.min_cycles:
            return None

        # Calculate actual cycle lengths by comparing consecutive start dates
        cycle_lengths = []
        for i in range(len(all_cycles) - 1):
            current_cycle = all_cycles[i]
            next_cycle = all_cycles[i + 1]
            # Cycle length is from start of this cycle to start of next cycle
            length = (next_cycle.start_date - current_cycle.start_date).days
            cycle_lengths.append(length)

        if not cycle_lengths:
            return None

        avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)
        avg_period_length = self._calculate_average_period_length(all_cycles)

        # Get last (most recent) cycle start date
        last_cycle = all_cycles[-1]  # Last item in ordered list
        predicted_start = last_cycle.start_date + timedelta(days=int(avg_cycle_length))
        predicted_end = predicted_start + timedelta(days=int(avg_period_length) - 1)

        # Calculate ovulation (typically 14 days before next period)
        predicted_ovulation = predicted_start - timedelta(days=14)
        fertile_window_start = predicted_ovulation - timedelta(days=2)
        fertile_window_end = predicted_ovulation + timedelta(days=2)

        # Calculate confidence score based on cycle regularity
        confidence = self._calculate_confidence(cycle_lengths)

        # Deactivate old predictions
        CyclePrediction.objects.filter(user=self.user, is_active=True).update(is_active=False)

        # Create new prediction
        prediction = CyclePrediction.objects.create(
            user=self.user,
            predicted_period_start=predicted_start,
            predicted_period_end=predicted_end,
            predicted_ovulation_date=predicted_ovulation,
            predicted_fertile_window_start=fertile_window_start,
            predicted_fertile_window_end=fertile_window_end,
            confidence_score=confidence,
            algorithm_used='average',
            based_on_cycles_count=len(cycle_lengths),
            is_active=True,
        )

        return prediction

    def _calculate_average_period_length(self, cycles) -> int:
        """Calculate average period length from cycles."""
        period_lengths = [c.period_length for c in cycles if c.period_length]
        if period_lengths:
            return int(sum(period_lengths) / len(period_lengths))
        return settings.CYCLE_TRACKING_CONFIG.get('DEFAULT_CYCLE_LENGTH', 28)

    def _calculate_confidence(self, cycle_lengths: list) -> Decimal:
        """
        Calculate confidence score based on cycle regularity.

        Returns value between 0 and 1.
        """
        if len(cycle_lengths) < 2:
            return Decimal('0.5')

        # Calculate standard deviation
        mean = sum(cycle_lengths) / len(cycle_lengths)
        variance = sum((x - mean) ** 2 for x in cycle_lengths) / len(cycle_lengths)
        std_dev = variance ** 0.5

        # Lower std dev = higher confidence
        # Assuming std dev of 0 = confidence 1.0, std dev of 7+ = confidence 0.0
        confidence = max(0, 1 - (std_dev / 7))
        return Decimal(str(round(confidence, 2)))


class StatisticsService:
    """
    Service for calculating and updating cycle statistics.
    """

    def __init__(self, user):
        self.user = user

    def calculate_statistics(self) -> CycleStatistics:
        """
        Calculate or update cycle statistics for the user.
        """
        # Get all cycles ordered by start date
        all_cycles = list(Cycle.objects.filter(user=self.user).order_by('start_date'))

        # Get or create statistics object
        stats, _ = CycleStatistics.objects.get_or_create(user=self.user)

        # Calculate actual cycle lengths from consecutive start dates
        if len(all_cycles) >= 2:
            cycle_lengths = []
            for i in range(len(all_cycles) - 1):
                current_cycle = all_cycles[i]
                next_cycle = all_cycles[i + 1]
                length = (next_cycle.start_date - current_cycle.start_date).days
                cycle_lengths.append(length)

            if cycle_lengths:
                stats.average_cycle_length = Decimal(str(round(sum(cycle_lengths) / len(cycle_lengths), 2)))
                stats.shortest_cycle_length = min(cycle_lengths)
                stats.longest_cycle_length = max(cycle_lengths)
                stats.cycle_regularity_score = self._calculate_regularity_score(cycle_lengths)

            # Calculate period statistics from end_date (which represents period end)
            # Period length = days from start to end of period
            period_lengths = []
            for cycle in all_cycles:
                if cycle.end_date:
                    period_len = (cycle.end_date - cycle.start_date).days + 1
                    period_lengths.append(period_len)

            if period_lengths:
                stats.average_period_length = Decimal(str(round(sum(period_lengths) / len(period_lengths), 2)))
                stats.shortest_period_length = min(period_lengths)
                stats.longest_period_length = max(period_lengths)

        stats.total_cycles_tracked = len(all_cycles)
        stats.complete_cycles_count = sum(1 for c in all_cycles if c.end_date)
        stats.save()

        return stats

    def _calculate_regularity_score(self, cycle_lengths: list) -> Decimal:
        """
        Calculate a regularity score (0-1) based on cycle length variance.
        """
        if len(cycle_lengths) < 2:
            return Decimal('0.5')

        mean = sum(cycle_lengths) / len(cycle_lengths)
        variance = sum((x - mean) ** 2 for x in cycle_lengths) / len(cycle_lengths)
        std_dev = variance ** 0.5

        # Lower variance = higher regularity
        regularity = max(0, 1 - (std_dev / 10))
        return Decimal(str(round(regularity, 2)))


class InsightService:
    """
    Service for generating insights and recommendations.
    """

    def __init__(self, user):
        self.user = user

    def generate_insights(self):
        """
        Generate insights based on user's cycle data.
        """
        insights = []

        # Check cycle regularity
        stats = CycleStatistics.objects.filter(user=self.user).first()
        if stats and stats.total_cycles_tracked >= 3:
            if stats.cycle_regularity_score < Decimal('0.5'):
                insights.append({
                    'category': 'cycle',
                    'priority': 'medium',
                    'title': 'Irregular Cycle Pattern Detected',
                    'description': (
                        f'Your cycles vary significantly (between {stats.shortest_cycle_length} '
                        f'and {stats.longest_cycle_length} days). Consider consulting with a '
                        'healthcare provider if this concerns you.'
                    ),
                })

        # Check for common symptom patterns
        recent_logs = DailyLog.objects.filter(user=self.user).order_by('-date')[:30]
        if recent_logs.exists():
            mood_counts = {}
            for log in recent_logs:
                if log.mood:
                    mood_counts[log.mood] = mood_counts.get(log.mood, 0) + 1

            # If predominantly bad moods
            bad_moods = mood_counts.get('bad', 0) + mood_counts.get('terrible', 0)
            if bad_moods > len(recent_logs) * 0.5:
                insights.append({
                    'category': 'mood',
                    'priority': 'high',
                    'title': 'Mood Pattern Needs Attention',
                    'description': (
                        'You\'ve been experiencing predominantly negative moods. Consider '
                        'speaking with a healthcare provider about your emotional wellbeing.'
                    ),
                })

        # Create insight records
        for insight_data in insights:
            Insight.objects.create(
                user=self.user,
                **insight_data,
                based_on_data_until=timezone.now().date()
            )

        return insights
