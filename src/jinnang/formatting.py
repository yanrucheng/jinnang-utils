import math
import logging
from string import Formatter

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