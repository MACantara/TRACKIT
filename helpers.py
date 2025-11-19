"""
Helper utilities for TRACKIT Flask app.
"""

from datetime import datetime
from dateutil import parser as date_parser

def parse_date(date_string):
    """Parse ISO date string to datetime object."""
    if not date_string:
        return None
    try:
        if isinstance(date_string, str):
            return date_parser.parse(date_string)
        return date_string
    except:
        return None

def format_date(date_value, format_string='%Y-%m-%d'):
    """Format date value to string."""
    if not date_value:
        return ''
    try:
        if isinstance(date_value, str):
            dt = date_parser.parse(date_value)
        else:
            dt = date_value
        return dt.strftime(format_string)
    except:
        return str(date_value)
