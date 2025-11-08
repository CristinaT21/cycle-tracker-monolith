"""
Views for the Analytics module.
"""

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from .models import CyclePrediction, CycleStatistics, Insight
from .serializers import (
    CyclePredictionSerializer,
    CycleStatisticsSerializer,
    InsightSerializer,
    InsightUpdateSerializer,
)
from .services import PredictionService, StatisticsService, InsightService
from shared.utils import format_response


@extend_schema(tags=['Analytics'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_prediction(request):
    """
    Get the current active prediction for the user.
    """
    try:
        prediction = CyclePrediction.objects.get(user=request.user, is_active=True)
        serializer = CyclePredictionSerializer(prediction)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)
    except CyclePrediction.DoesNotExist:
        return Response(
            {'success': False, 'message': 'No active prediction found. Generate one first.'},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(tags=['Analytics'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_prediction(request):
    """
    Generate a new prediction for the user's next cycle.
    """
    service = PredictionService(request.user)
    prediction = service.generate_prediction()

    if prediction:
        serializer = CyclePredictionSerializer(prediction)
        return Response(
            format_response(serializer.data, message="Prediction generated successfully"),
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {
                'success': False,
                'message': 'Insufficient data to generate prediction. Please track at least 3 complete cycles.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(tags=['Analytics'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistics(request):
    """
    Get cycle statistics for the user.
    """
    try:
        statistics = CycleStatistics.objects.get(user=request.user)
        serializer = CycleStatisticsSerializer(statistics)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)
    except CycleStatistics.DoesNotExist:
        return Response(
            {'success': False, 'message': 'No statistics available. Calculate them first.'},
            status=status.HTTP_404_NOT_FOUND
        )


@extend_schema(tags=['Analytics'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_statistics(request):
    """
    Calculate or recalculate cycle statistics for the user.
    """
    service = StatisticsService(request.user)
    statistics = service.calculate_statistics()
    serializer = CycleStatisticsSerializer(statistics)
    return Response(
        format_response(serializer.data, message="Statistics calculated successfully"),
        status=status.HTTP_200_OK
    )


class InsightViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing insights.
    """

    serializer_class = InsightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return insights for the current user only."""
        return Insight.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['update', 'partial_update', 'mark_as_read', 'dismiss']:
            return InsightUpdateSerializer
        return InsightSerializer

    @extend_schema(tags=['Insights'])
    def list(self, request, *args, **kwargs):
        """List all insights for the current user."""
        queryset = self.get_queryset().filter(is_dismissed=False)
        unread = queryset.filter(is_read=False)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            format_response({
                'insights': serializer.data,
                'unread_count': unread.count(),
            }),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Insights'])
    def retrieve(self, request, *args, **kwargs):
        """Get a specific insight."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(tags=['Insights'])
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark an insight as read."""
        insight = self.get_object()
        insight.is_read = True
        insight.read_at = timezone.now()
        insight.save()

        serializer = InsightSerializer(insight)
        return Response(
            format_response(serializer.data, message="Insight marked as read"),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Insights'])
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss an insight."""
        insight = self.get_object()
        insight.is_dismissed = True
        insight.save()

        return Response(
            format_response(None, message="Insight dismissed"),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Insights'])
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate new insights for the user."""
        service = InsightService(request.user)
        insights = service.generate_insights()

        return Response(
            format_response(
                {'generated_count': len(insights)},
                message=f"Generated {len(insights)} new insights"
            ),
            status=status.HTTP_201_CREATED
        )
