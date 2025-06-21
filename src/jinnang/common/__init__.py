"""Common class definitions for jinnang utility package.

This submodule contains reusable class definitions that provide design patterns and
formatting utilities used throughout the jinnang package and its consumers.

Modules:
    - patterns: Design pattern implementations (Singleton, Factory, etc.)
    - formatters: Data formatting and display utilities
    - decorators: Function decorators for behavior modification
"""

# Import all classes for easy access
from .formatters import TruncatedPrettyPrinter, ResolutionPreset, Verbosity, get_numeric
from .patterns import GenericSingletonFactory
from .decorators import mock_when, fail_recover, custom_retry, BadInputException
from .collections import list_to_tuple, get_unique_key

# Export all classes
__all__ = [
    'TruncatedPrettyPrinter',
    'ResolutionPreset', 
    'Verbosity',
    'GenericSingletonFactory',
    'mock_when',
    'fail_recover',
    'custom_retry',
    'BadInputException',
    'list_to_tuple',
    'get_numeric',
    'get_unique_key'
]