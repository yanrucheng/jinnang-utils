"""Common class definitions for jinnang utility package.

This submodule contains reusable class definitions that provide design patterns and
formatting utilities used throughout the jinnang package and its consumers.

Modules:
    - patterns: Design pattern implementations (Singleton, Factory, etc.)
    - formatters: Data formatting and display utilities
    - decorators: Function decorators for behavior modification
"""

# Import all classes for easy access
from .formatters import TruncatedPrettyPrinter, ResolutionPreset, Verbosity
from .patterns import GenericSingletonFactory
from .decorators import mock_when, fail_recover, custom_retry, BadInputException

# Export all classes
__all__ = [
    'TruncatedPrettyPrinter',
    'ResolutionPreset', 
    'Verbosity',
    'GenericSingletonFactory',
    'mock_when',
    'fail_recover',
    'custom_retry',
    'BadInputException'
]