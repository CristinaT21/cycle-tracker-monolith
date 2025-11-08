"""
Custom middleware for cross-cutting concerns.
"""

import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all incoming requests and their processing time.
    """

    def process_request(self, request):
        """Log the start of request processing."""
        request.start_time = time.time()
        logger.info(f"Started {request.method} {request.path}")
        return None

    def process_response(self, request, response):
        """Log the completion of request processing."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Completed {request.method} {request.path} "
                f"[{response.status_code}] in {duration:.2f}s"
            )
        return response


class ModuleBoundaryMiddleware(MiddlewareMixin):
    """
    Middleware to enforce module boundaries and track inter-module communication.

    This is primarily for monitoring and can help identify tight coupling.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Track which module is handling the request."""
        module_name = view_func.__module__.split('.')[1] if '.' in view_func.__module__ else 'unknown'
        request.handling_module = module_name
        return None
