"""
URL routing for the Analytics module.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analytics'

router = DefaultRouter()
router.register(r'insights', views.InsightViewSet, basename='insight')

urlpatterns = [
    # Prediction endpoints
    path('predictions/current/', views.get_current_prediction, name='current_prediction'),
    path('predictions/generate/', views.generate_prediction, name='generate_prediction'),

    # Statistics endpoints
    path('statistics/', views.get_statistics, name='statistics'),
    path('statistics/calculate/', views.calculate_statistics, name='calculate_statistics'),

    # Router URLs (insights)
    path('', include(router.urls)),
]
