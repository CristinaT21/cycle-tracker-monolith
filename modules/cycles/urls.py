"""
URL routing for the Cycles module.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'cycles'

router = DefaultRouter()
router.register(r'', views.CycleViewSet, basename='cycle')
router.register(r'logs', views.DailyLogViewSet, basename='daily-log')

urlpatterns = [
    # Symptoms endpoint
    path('symptoms/', views.list_symptoms, name='symptoms'),

    # Router URLs
    path('', include(router.urls)),
]
