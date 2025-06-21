import math
import logging
from string import Formatter
from typing import Optional

import pytz
from dateutil import parser

# Import classes from the common submodule
from .common.formatters import ResolutionPreset, Verbosity, TruncatedPrettyPrinter

logger = logging.getLogger(__name__)

# LLM Token calculation
def calculate_tokens(width: int, height: int) -> float:
    """Calculate tokens as (h * w) / 784"""
    return math.ceil((width * height) / 784)


# TruncatedPrettyPrinter is now imported from common submodule


def safe_format(template: str, data: dict) -> str:
    """Safely format a string using only the keys present in the template.
    
    Args:
        template (str): String with placeholders (e.g., 'Hello {name}').
        data (dict): Dictionary containing key-value pairs for formatting.
    
    Returns:
        str: Formatted string with only the required keys applied.
        
    Example:
        >>> safe_format('a {haha}', {'haha': 1, 'eheh': 2})
        'a 1'
    """
    required_keys = [fn for _, fn, _, _ in Formatter().parse(template) if fn is not None]
    filtered_data = {k: data[k] for k in required_keys if k in data}
    return template.format(**filtered_data)

def date_str_to_iso_date_str(date_str: Optional[str], target_timezone: str = 'Asia/Shanghai') -> Optional[str]:
    if not date_str:
        return None
    try:
        if ' ' in date_str:
            parts = date_str.split(' ')
            if len(parts) > 0 and parts[0].count(':') > 0:
                parts[0] = parts[0].replace(':', '-', 2)
                date_str = ' '.join(parts)
        dt = parser.parse(date_str)
        if dt.microsecond:
            dt = dt.replace(microsecond=0)
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        target_tz = pytz.timezone(target_timezone)
        localized = dt.astimezone(target_tz)
        return localized.isoformat(timespec='seconds')
    except Exception:
        return None


def get_int(value, default=0):
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default