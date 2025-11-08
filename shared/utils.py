"""
Shared utility functions used across modules.
"""

from datetime import datetime, timedelta
from typing import Optional


def calculate_date_difference(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate the number of days between two dates.

    Args:
        start_date: The starting date
        end_date: The ending date

    Returns:
        Number of days between the dates
    """
    return (end_date - start_date).days


def get_next_date(base_date: datetime, days: int) -> datetime:
    """
    Get a date that is a specified number of days from a base date.

    Args:
        base_date: The starting date
        days: Number of days to add

    Returns:
        The calculated date
    """
    return base_date + timedelta(days=days)


def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """
    Validate that a date range is valid (start before end).

    Args:
        start_date: The starting date
        end_date: The ending date

    Returns:
        True if valid, False otherwise
    """
    return start_date <= end_date


def format_response(data, message: Optional[str] = None, success: bool = True):
    """
    Format a standard API response.

    Args:
        data: The response data
        message: Optional message
        success: Whether the operation was successful

    Returns:
        Formatted response dictionary
    """
    response = {
        'success': success,
        'data': data,
    }
    if message:
        response['message'] = message
    return response
