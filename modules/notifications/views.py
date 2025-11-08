"""
Views for the Notifications module.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from .models import Notification, ReminderSchedule, NotificationPreference
from .serializers import (
    NotificationSerializer,
    ReminderScheduleSerializer,
    NotificationPreferenceSerializer,
)
from shared.utils import format_response


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing notifications.

    Provides read-only access to user notifications.
    """

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'channel', 'is_read']
    ordering_fields = ['scheduled_for', 'created_at']
    ordering = ['-scheduled_for']

    def get_queryset(self):
        """Return notifications for the current user only."""
        return Notification.objects.filter(user=self.request.user)

    @extend_schema(tags=['Notifications'])
    def list(self, request, *args, **kwargs):
        """List all notifications for the current user."""
        queryset = self.filter_queryset(self.get_queryset())
        unread_count = queryset.filter(is_read=False).count()

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            format_response({
                'notifications': serializer.data,
                'unread_count': unread_count,
            }),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Notifications'])
    def retrieve(self, request, *args, **kwargs):
        """Get a specific notification."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(tags=['Notifications'])
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

        serializer = self.get_serializer(notification)
        return Response(
            format_response(serializer.data, message="Notification marked as read"),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Notifications'])
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read."""
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())

        return Response(
            format_response(
                {'updated_count': updated_count},
                message=f"Marked {updated_count} notifications as read"
            ),
            status=status.HTTP_200_OK
        )


class ReminderScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reminder schedules.
    """

    serializer_class = ReminderScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return reminder schedules for the current user only."""
        return ReminderSchedule.objects.filter(user=self.request.user)

    @extend_schema(tags=['Reminders'])
    def list(self, request, *args, **kwargs):
        """List all reminder schedules for the current user."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(format_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(tags=['Reminders'])
    def create(self, request, *args, **kwargs):
        """Create a new reminder schedule."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reminder = serializer.save(user=request.user)

        return Response(
            format_response(
                ReminderScheduleSerializer(reminder).data,
                message="Reminder schedule created successfully"
            ),
            status=status.HTTP_201_CREATED
        )

    @extend_schema(tags=['Reminders'])
    def update(self, request, *args, **kwargs):
        """Update a reminder schedule."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        reminder = serializer.save()

        return Response(
            format_response(
                ReminderScheduleSerializer(reminder).data,
                message="Reminder schedule updated successfully"
            ),
            status=status.HTTP_200_OK
        )

    @extend_schema(tags=['Reminders'])
    def destroy(self, request, *args, **kwargs):
        """Delete a reminder schedule."""
        instance = self.get_object()
        instance.delete()
        return Response(
            format_response(None, message="Reminder schedule deleted successfully"),
            status=status.HTTP_204_NO_CONTENT
        )


@extend_schema(tags=['Notification Preferences'])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification_preferences(request):
    """
    Get notification preferences for the current user.
    """
    preferences, created = NotificationPreference.objects.get_or_create(user=request.user)
    serializer = NotificationPreferenceSerializer(preferences)
    return Response(format_response(serializer.data), status=status.HTTP_200_OK)


@extend_schema(tags=['Notification Preferences'])
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_notification_preferences(request):
    """
    Update notification preferences for the current user.
    """
    preferences, created = NotificationPreference.objects.get_or_create(user=request.user)
    partial = request.method == 'PATCH'
    serializer = NotificationPreferenceSerializer(preferences, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(
            format_response(serializer.data, message="Preferences updated successfully"),
            status=status.HTTP_200_OK
        )
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
