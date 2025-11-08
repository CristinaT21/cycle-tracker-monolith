"""
Views for the Visualizations module.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .services import (
    CycleVisualizationService,
    SymptomVisualizationService,
    MoodVisualizationService,
)
from shared.utils import format_response


@extend_schema(
    tags=['Visualizations - Cycles'],
    parameters=[
        OpenApiParameter(name='months', description='Number of months of history', required=False, type=int)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cycle_length_history(request):
    """
    Get cycle length history for line chart visualization.

    Query Parameters:
        - months: Number of months to include (default: 6)
    """
    months = int(request.query_params.get('months', 6))
    service = CycleVisualizationService(request.user)
    data = service.get_cycle_length_history(months)

    return Response(format_response(data), status=status.HTTP_200_OK)


@extend_schema(
    tags=['Visualizations - Cycles'],
    parameters=[
        OpenApiParameter(name='year', description='Year', required=True, type=int),
        OpenApiParameter(name='month', description='Month (1-12)', required=True, type=int)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cycle_calendar(request):
    """
    Get cycle data for calendar visualization.

    Query Parameters:
        - year: Year (e.g., 2024)
        - month: Month (1-12)
    """
    year = int(request.query_params.get('year'))
    month = int(request.query_params.get('month'))

    if not (1 <= month <= 12):
        return Response(
            {'success': False, 'message': 'Month must be between 1 and 12'},
            status=status.HTTP_400_BAD_REQUEST
        )

    service = CycleVisualizationService(request.user)
    data = service.get_cycle_calendar_data(year, month)

    return Response(format_response(data), status=status.HTTP_200_OK)


@extend_schema(tags=['Visualizations - Cycles'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cycle_statistics_chart(request):
    """
    Get cycle statistics for bar/radar chart visualization.
    """
    service = CycleVisualizationService(request.user)
    data = service.get_cycle_statistics_chart()

    return Response(format_response(data), status=status.HTTP_200_OK)


@extend_schema(
    tags=['Visualizations - Symptoms'],
    parameters=[
        OpenApiParameter(name='days', description='Number of days to analyze', required=False, type=int)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symptom_frequency(request):
    """
    Get symptom frequency for bar chart visualization.

    Query Parameters:
        - days: Number of days to include (default: 90)
    """
    days = int(request.query_params.get('days', 90))
    service = SymptomVisualizationService(request.user)
    data = service.get_symptom_frequency(days)

    return Response(format_response(data), status=status.HTTP_200_OK)


@extend_schema(tags=['Visualizations - Symptoms'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def symptom_by_phase(request):
    """
    Get symptom distribution by cycle phase.
    """
    service = SymptomVisualizationService(request.user)
    data = service.get_symptom_by_cycle_phase()

    return Response(format_response(data), status=status.HTTP_200_OK)


@extend_schema(
    tags=['Visualizations - Mood'],
    parameters=[
        OpenApiParameter(name='days', description='Number of days to analyze', required=False, type=int)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mood_timeline(request):
    """
    Get mood data over time for timeline visualization.

    Query Parameters:
        - days: Number of days to include (default: 30)
    """
    days = int(request.query_params.get('days', 30))
    service = MoodVisualizationService(request.user)
    data = service.get_mood_timeline(days)

    return Response(format_response(data), status=status.HTTP_200_OK)


@extend_schema(
    tags=['Visualizations - Mood'],
    parameters=[
        OpenApiParameter(name='days', description='Number of days to analyze', required=False, type=int)
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mood_distribution(request):
    """
    Get mood distribution for pie/doughnut chart.

    Query Parameters:
        - days: Number of days to include (default: 90)
    """
    days = int(request.query_params.get('days', 90))
    service = MoodVisualizationService(request.user)
    data = service.get_mood_distribution(days)

    return Response(format_response(data), status=status.HTTP_200_OK)
