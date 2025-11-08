"""
URL routing for the Visualizations module.
"""

from django.urls import path
from . import views

app_name = 'visualizations'

urlpatterns = [
    # Cycle visualizations
    path('cycles/history/', views.cycle_length_history, name='cycle_history'),
    path('cycles/calendar/', views.cycle_calendar, name='cycle_calendar'),
    path('cycles/statistics/', views.cycle_statistics_chart, name='cycle_statistics'),

    # Symptom visualizations
    path('symptoms/frequency/', views.symptom_frequency, name='symptom_frequency'),
    path('symptoms/by-phase/', views.symptom_by_phase, name='symptom_by_phase'),

    # Mood visualizations
    path('mood/timeline/', views.mood_timeline, name='mood_timeline'),
    path('mood/distribution/', views.mood_distribution, name='mood_distribution'),
]
