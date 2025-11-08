"""
Views for the Cycles module.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema

from .models import Cycle, PeriodDay, Symptom, DailyLog
from .serializers import (
    CycleSerializer,
    CycleCreateSerializer,
    PeriodDaySerializer,
    SymptomSerializer,
    DailyLogSerializer,
)
from shared.utils import format_response
from shared.exceptions import NotFoundException


class CycleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing menstrual cycles.

    Provides CRUD operations for cycle tracking.
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active', 'start_date']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return CycleCreateSerializer
        return CycleSerializer

    def get_queryset(self):
        """Return cycles for the current user only."""
        return Cycle.objects.filter(user=self.request.user).prefetch_related('period_days')

    @extend_schema(tags=['Cycles'])
    def list(self, request, *args, **kwargs):
        """List all cycles for the current user."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(tags=['Cycles'])
    def create(self, request, *args, **kwargs):
        """Create a new cycle."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cycle = serializer.save()
        return Response(
            format_response(
                CycleSerializer(cycle).data,
                message="Cycle created successfully"
            ),
            status=status.HTTP_201_CREATED
        )

    @extend_schema(tags=['Cycles'])
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific cycle."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(tags=['Cycles'])
    def update(self, request, *args, **kwargs):
        """Update a cycle."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        cycle = serializer.save()

        # Recalculate cycle length if end date was updated
        if 'end_date' in request.data:
            cycle.calculate_cycle_length()
            cycle.save()

        return Response(
            format_response(
                CycleSerializer(cycle).data,
                message="Cycle updated successfully"
            ),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Cycles'])
    @action(detail=True, methods=['post'])
    def add_period_day(self, request, pk=None):
        """Add a period day to a cycle."""
        cycle = self.get_object()
        serializer = PeriodDaySerializer(data=request.data)

        if serializer.is_valid():
            period_day = serializer.save(cycle=cycle)
            return Response(
                format_response(
                    PeriodDaySerializer(period_day).data,
                    message="Period day added successfully"
                ),
                status=status.HTTP_201_CREATED
            )
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Cycles'])
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get the current active cycle."""
        try:
            cycle = Cycle.objects.get(user=request.user, is_active=True)
            serializer = self.get_serializer(cycle)
            return Response(format_response(serializer.data), status=status.HTTP_200_OK)
        except Cycle.DoesNotExist:
            return Response(
                {'success': False, 'message': 'No active cycle found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DailyLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing daily logs.

    Provides CRUD operations for daily symptom and mood tracking.
    """

    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['date', 'mood']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        """Return daily logs for the current user only."""
        return DailyLog.objects.filter(user=self.request.user).prefetch_related('symptoms')

    @extend_schema(tags=['Daily Logs'])
    def list(self, request, *args, **kwargs):
        """List all daily logs for the current user."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(tags=['Daily Logs'])
    def create(self, request, *args, **kwargs):
        """Create a new daily log."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        daily_log = serializer.save()
        return Response(
            format_response(
                DailyLogSerializer(daily_log).data,
                message="Daily log created successfully"
            ),
            status=status.HTTP_201_CREATED
        )


@extend_schema(tags=['Symptoms'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_symptoms(request):
    """
    List all available symptoms for tracking.
    """
    symptoms = Symptom.objects.filter(is_active=True)
    serializer = SymptomSerializer(symptoms, many=True)
    return Response(format_response(serializer.data), status=status.HTTP_200_OK)
