"""
Services for aggregating data for visualizations.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from django.db.models import Avg, Count, Q
from collections import defaultdict

from modules.cycles.models import Cycle, DailyLog
from modules.analytics.models import CycleStatistics


class CycleVisualizationService:
    """
    Service for generating cycle-related visualization data.
    """

    def __init__(self, user):
        self.user = user

    def get_cycle_length_history(self, months: int = 6) -> Dict[str, Any]:
        """
        Get cycle length history for the specified number of months.

        Returns data suitable for a line chart showing cycle length over time.
        """
        cutoff_date = datetime.now().date() - timedelta(days=months * 30)
        cycles = Cycle.objects.filter(
            user=self.user,
            start_date__gte=cutoff_date,
            cycle_length__isnull=False
        ).order_by('start_date')

        data = {
            'labels': [],
            'datasets': [{
                'label': 'Cycle Length (days)',
                'data': [],
            }]
        }

        for cycle in cycles:
            data['labels'].append(cycle.start_date.strftime('%Y-%m-%d'))
            data['datasets'][0]['data'].append(cycle.cycle_length)

        return data

    def get_cycle_calendar_data(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get cycle data for a specific month for calendar visualization.

        Returns:
            Dictionary with dates and their cycle phases
        """
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()

        calendar_data = {}

        # Get cycles that overlap with this month
        cycles = Cycle.objects.filter(
            user=self.user,
            start_date__lte=end_date,
        ).filter(
            Q(end_date__gte=start_date) | Q(end_date__isnull=True)
        )

        for cycle in cycles:
            # Mark period days
            current_date = max(cycle.start_date, start_date)
            cycle_end = cycle.end_date if cycle.end_date else end_date

            while current_date < min(cycle_end, end_date):
                if current_date >= start_date:
                    # Determine phase
                    days_into_cycle = (current_date - cycle.start_date).days + 1

                    if cycle.period_length and days_into_cycle <= cycle.period_length:
                        phase = 'period'
                    elif cycle.cycle_length:
                        # Estimate ovulation around day 14 before next cycle
                        ovulation_day = cycle.cycle_length - 14
                        if abs(days_into_cycle - ovulation_day) <= 1:
                            phase = 'ovulation'
                        elif ovulation_day - 3 <= days_into_cycle <= ovulation_day + 1:
                            phase = 'fertile'
                        else:
                            phase = 'normal'
                    else:
                        phase = 'normal'

                    calendar_data[current_date.strftime('%Y-%m-%d')] = {
                        'phase': phase,
                        'day_of_cycle': days_into_cycle,
                    }

                current_date += timedelta(days=1)

        return calendar_data

    def get_cycle_statistics_chart(self) -> Dict[str, Any]:
        """
        Get comparative statistics for visualization.

        Returns data suitable for a bar chart or radar chart.
        """
        try:
            stats = CycleStatistics.objects.get(user=self.user)

            data = {
                'labels': [
                    'Average Cycle Length',
                    'Shortest Cycle',
                    'Longest Cycle',
                    'Average Period Length',
                ],
                'datasets': [{
                    'label': 'Days',
                    'data': [
                        float(stats.average_cycle_length),
                        stats.shortest_cycle_length,
                        stats.longest_cycle_length,
                        float(stats.average_period_length),
                    ]
                }],
                'metadata': {
                    'total_cycles': stats.total_cycles_tracked,
                    'regularity_score': float(stats.cycle_regularity_score),
                }
            }

            return data
        except CycleStatistics.DoesNotExist:
            return {
                'labels': [],
                'datasets': [],
                'metadata': {'error': 'No statistics available'}
            }


class SymptomVisualizationService:
    """
    Service for generating symptom-related visualization data.
    """

    def __init__(self, user):
        self.user = user

    def get_symptom_frequency(self, days: int = 90) -> Dict[str, Any]:
        """
        Get symptom frequency over the specified period.

        Returns data suitable for a bar chart showing most common symptoms.
        """
        cutoff_date = datetime.now().date() - timedelta(days=days)
        logs = DailyLog.objects.filter(
            user=self.user,
            date__gte=cutoff_date
        ).prefetch_related('symptoms')

        symptom_counts = defaultdict(int)
        for log in logs:
            for symptom in log.symptoms.all():
                symptom_counts[symptom.name] += 1

        # Sort by frequency
        sorted_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        data = {
            'labels': [s[0] for s in sorted_symptoms],
            'datasets': [{
                'label': 'Frequency',
                'data': [s[1] for s in sorted_symptoms],
            }]
        }

        return data

    def get_symptom_by_cycle_phase(self) -> Dict[str, Any]:
        """
        Get symptom distribution across different cycle phases.

        Returns data showing which symptoms are most common in which phase.
        """
        # Get recent completed cycles
        cycles = Cycle.objects.filter(
            user=self.user,
            end_date__isnull=False
        ).order_by('-start_date')[:3]

        phase_symptoms = {
            'period': defaultdict(int),
            'follicular': defaultdict(int),
            'ovulation': defaultdict(int),
            'luteal': defaultdict(int),
        }

        for cycle in cycles:
            if not cycle.cycle_length:
                continue

            logs = DailyLog.objects.filter(
                user=self.user,
                cycle=cycle
            ).prefetch_related('symptoms')

            for log in logs:
                days_into_cycle = (log.date - cycle.start_date).days + 1

                # Determine phase
                if cycle.period_length and days_into_cycle <= cycle.period_length:
                    phase = 'period'
                elif days_into_cycle <= cycle.cycle_length // 2:
                    phase = 'follicular'
                elif abs(days_into_cycle - (cycle.cycle_length - 14)) <= 2:
                    phase = 'ovulation'
                else:
                    phase = 'luteal'

                for symptom in log.symptoms.all():
                    phase_symptoms[phase][symptom.name] += 1

        return {
            'phases': list(phase_symptoms.keys()),
            'symptoms': phase_symptoms,
        }


class MoodVisualizationService:
    """
    Service for generating mood-related visualization data.
    """

    def __init__(self, user):
        self.user = user

    def get_mood_timeline(self, days: int = 30) -> Dict[str, Any]:
        """
        Get mood data over time for timeline visualization.
        """
        cutoff_date = datetime.now().date() - timedelta(days=days)
        logs = DailyLog.objects.filter(
            user=self.user,
            date__gte=cutoff_date,
            mood__isnull=False
        ).order_by('date')

        mood_values = {
            'great': 5,
            'good': 4,
            'okay': 3,
            'bad': 2,
            'terrible': 1,
        }

        data = {
            'labels': [],
            'datasets': [{
                'label': 'Mood Score',
                'data': [],
            }]
        }

        for log in logs:
            data['labels'].append(log.date.strftime('%Y-%m-%d'))
            data['datasets'][0]['data'].append(mood_values.get(log.mood, 3))

        return data

    def get_mood_distribution(self, days: int = 90) -> Dict[str, Any]:
        """
        Get mood distribution as percentages for pie/doughnut chart.
        """
        cutoff_date = datetime.now().date() - timedelta(days=days)
        mood_counts = DailyLog.objects.filter(
            user=self.user,
            date__gte=cutoff_date,
            mood__isnull=False
        ).values('mood').annotate(count=Count('mood'))

        data = {
            'labels': [],
            'datasets': [{
                'label': 'Mood Distribution',
                'data': [],
            }]
        }

        for item in mood_counts:
            data['labels'].append(item['mood'].capitalize())
            data['datasets'][0]['data'].append(item['count'])

        return data
