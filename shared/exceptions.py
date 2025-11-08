"""
Custom exceptions and exception handling for the application.

Provides consistent error handling across all modules.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


class BaseApplicationException(Exception):
    """Base exception for all application-specific exceptions."""

    default_message = "An application error occurred"
    default_code = "application_error"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=None, code=None, status_code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class ValidationException(BaseApplicationException):
    """Raised when validation fails."""

    default_message = "Validation failed"
    default_code = "validation_error"
    status_code = status.HTTP_400_BAD_REQUEST


class NotFoundException(BaseApplicationException):
    """Raised when a requested resource is not found."""

    default_message = "Resource not found"
    default_code = "not_found"
    status_code = status.HTTP_404_NOT_FOUND


class UnauthorizedException(BaseApplicationException):
    """Raised when authentication fails."""

    default_message = "Unauthorized access"
    default_code = "unauthorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(BaseApplicationException):
    """Raised when user doesn't have permission."""

    default_message = "Access forbidden"
    default_code = "forbidden"
    status_code = status.HTTP_403_FORBIDDEN


class ConflictException(BaseApplicationException):
    """Raised when there's a conflict with existing data."""

    default_message = "Resource conflict"
    default_code = "conflict"
    status_code = status.HTTP_409_CONFLICT


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST framework.

    Provides consistent error response format across the application.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Handle custom application exceptions
    if isinstance(exc, BaseApplicationException):
        logger.error(f"{exc.__class__.__name__}: {exc.message}", exc_info=True)
        return Response(
            {
                'error': {
                    'code': exc.code,
                    'message': exc.message,
                }
            },
            status=exc.status_code
        )

    # If response is None, it's an unhandled exception
    if response is None:
        logger.exception("Unhandled exception occurred", exc_info=True)
        return Response(
            {
                'error': {
                    'code': 'internal_server_error',
                    'message': 'An unexpected error occurred. Please try again later.',
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Customize the response format for DRF exceptions
    if hasattr(response, 'data'):
        custom_response_data = {
            'error': {
                'code': 'validation_error' if response.status_code == 400 else 'error',
                'message': response.data if isinstance(response.data, str) else response.data,
            }
        }
        response.data = custom_response_data

    return response
