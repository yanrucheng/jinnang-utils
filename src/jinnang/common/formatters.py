"""Formatting utility classes for data display and representation.

This module provides classes that help with formatting, displaying, and representing
data in various formats. It includes enumerations for common settings and specialized
formatters for improved data visualization.
"""

import math
import pprint
from enum import IntEnum, Enum
from functools import total_ordering
import logging
from typing import Any, Dict, List, Tuple, Union, Optional
from string import Formatter

logger = logging.getLogger(__name__)

@total_ordering
class ResolutionPreset(Enum):
    """Standard video resolution presets with exact dimensions.
    
    This enumeration defines common video resolution presets with their exact
    width and height dimensions in pixels. It supports comparison operations
    to determine relative sizes between resolutions.
    
    Each preset is represented as a tuple of (width, height) in pixels.
    The ORIGINAL preset is a special case that represents the native resolution
    of the source material (represented as None, None).
    
    Example:
        ```python
        # Compare resolutions
        if ResolutionPreset.RES_720P > ResolutionPreset.RES_480P:
            print("720p is higher resolution than 480p")
            
        # Get dimensions
        width, height = ResolutionPreset.RES_1080P.value
        ```
    """
    ORIGINAL = (None, None)

    RES_4K = (3840, 2160)
    RES_2K = (2560, 1440)
    RES_1080P = (1920, 1080)
    RES_720P = (1280, 720)
    RES_540P = (960, 540)
    RES_480P = (854, 480)
    RES_360P = (640, 360)
    RES_240P = (426, 240)

    RES_144P = (256, 144)       # Common low-quality streaming
    RES_120P = (160, 120)       # Old webcam/QQVGA standard
    RES_96P = (128, 96)         # Very low-res, sometimes for thumbnails
    RES_80P = (160, 80)         # Ultra-low bandwidth (e.g., IoT devices)
    RES_64P = (64, 64)          # Tiny (e.g., placeholder icons)
    RES_48P = (48, 48)          # Extremely small (practically unusable for video)
    RES_32P = (32, 32)          # Thumbnail/legacy icon size
    RES_16P = (16, 16)          # Smallest usable (favicon-sized)


    def __eq__(self, other):
        if not isinstance(other, ResolutionPreset):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, ResolutionPreset):
            return NotImplemented
        if self.value == (None, None):
            return False  # ORIGINAL is always largest
        if other.value == (None, None):
            return True
        return (self.value[0], self.value[1]) < (other.value[0], other.value[1])

class Verbosity(IntEnum):
    """Enumeration for controlling output verbosity levels.
    
    This enum provides standardized verbosity levels that can be used
    throughout the application to control the amount of information displayed
    to users or logged to files.
    
    Levels:
        SILENT (0): No output
        ONCE (1): Show only once or minimal information
        DETAIL (2): Show detailed information
        FULL (3): Show all available information
        TMP (4): Temporary/debug level (not for production use)
    """
    SILENT = 0
    ONCE = 1
    DETAIL = 2
    FULL = 3
    TMP = 4

class TruncatedPrettyPrinter(pprint.PrettyPrinter):
    """Enhanced pretty printer that truncates long collections.
    
    This class extends the standard PrettyPrinter to handle large collections
    (lists, tuples, sets) by showing only a subset of items from the beginning
    and end, with an indication of how many items were omitted in the middle.
    
    This is particularly useful for debugging or logging large data structures
    without overwhelming the output.
    """
    
    def __init__(self, *args, show_num: int = 6, **kwargs):
        """Initialize the TruncatedPrettyPrinter.
        
        Args:
            *args: Arguments to pass to the parent PrettyPrinter
            show_num: Number of items to show at the start and end of large collections
            **kwargs: Keyword arguments to pass to the parent PrettyPrinter
        """
        super().__init__(*args, **kwargs)
        self.show_num = show_num  # Number of items to show at start/end

    def _format(self, obj: Any, *args, **kwargs) -> Tuple[Optional[str], str]:
        """
        Format an object for pretty printing, with special handling for large collections.
        
        This method overrides the parent class's _format method to provide truncated
        representation of large collections (lists, tuples, sets). When a collection
        exceeds self.show_num items, only a subset of items from the beginning and end
        are shown, with an indication of how many items were omitted.
        
        Args:
            obj: The object to format
            *args: Additional positional arguments for the parent formatter
            **kwargs: Additional keyword arguments for the parent formatter
            
        Returns:
            Tuple[Optional[str], str]: A tuple containing the formatted representation
                as expected by the parent PrettyPrinter class
        """
        if isinstance(obj, (list, tuple, set)) and len(obj) > self.show_num:
            # Calculate items to show from start/end
            first_half = self.show_num // 2
            last_half = self.show_num - first_half
            start = obj[:first_half]
            end = obj[-last_half:]
            omitted = len(obj) - (first_half + last_half)
            
            # Format with line breaks and omission count
            separator = ',\n'
            items_start = separator.join(map(repr, start))
            items_end = separator.join(map(repr, end))
            
            res = 'default'
            if isinstance(obj, list):
                res = f"[\n{items_start},\n...<{omitted} items omitted>...,\n{items_end}\n]"
            elif isinstance(obj, tuple):
                res = f"(\n{items_start},\n...<{omitted} items omitted>...,\n{items_end}\n)"
            else:  # set
                res = f"{{\n{', '.join(map(repr, start))},\n...<{omitted} items omitted>...,\n{', '.join(map(repr, end))}\n}}"

            return None, res
        
        # Use the parent class's formatting for other types
        return super()._format(obj, *args, **kwargs)


def get_numeric(value):
    """Convert value to float if possible, else return None."""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None