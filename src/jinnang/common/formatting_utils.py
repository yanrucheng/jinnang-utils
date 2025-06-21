
import math
import logging
from .date import date_str_to_iso_date_str, timestamp_to_date
from string import Formatter
from typing import Optional



# Import Verbosity from the verbosity module
from .verbosity import Verbosity

logger = logging.getLogger(__name__)


def get_numeric(value):
    """Convert value to float if possible, else return None."""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None

# LLM Token calculation

def calculate_tokens(width: int, height: int) -> float:
    """Calculate tokens as (h * w) / 784"""
    return math.ceil((width * height) / 784)


# Token calculation for LLM processing
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




def get_int(value, default=0):
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

