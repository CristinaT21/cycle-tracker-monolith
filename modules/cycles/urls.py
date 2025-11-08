"""
URL routing for the Cycles module.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'cycles'

# Create separate routers to avoid URL conflicts
cycle_router = DefaultRouter()
cycle_router.register(r'', views.CycleViewSet, basename='cycle')

log_router = DefaultRouter()
log_router.register(r'', views.DailyLogViewSet, basename='daily-log')

urlpatterns = [
    # Symptoms endpoint
    path('symptoms/', views.list_symptoms, name='symptoms'),

    # Daily logs endpoints (separate path to avoid conflict)
    path('logs/', include(log_router.urls)),

    # Cycle endpoints at root
    path('', include(cycle_router.urls)),
]
