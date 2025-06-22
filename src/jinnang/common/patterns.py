"""Design pattern implementations for reuse across the jinnang package.

This module provides implementations of common design patterns such as Singleton,
Factory, and other structural patterns that can be reused throughout the application.
"""

import os
import logging
from typing import TypeVar, Type, Dict, Any, Optional, List, ClassVar

from jinnang.verbosity.verbosity import Verbosity

# Type variable for generic class methods
T = TypeVar('T')

class Singleton:
    """
    Base singleton class compatible with Python 3.8+.
    
    This class implements the Singleton pattern, ensuring only one instance 
    of a class exists and providing a standardized way to access it.
    
    Example:
        ```python
        class MyManager(Singleton):
            def __init__(self, config=None):
                if not hasattr(self, '_initialized'):
                    self.config = config or {}
                    self._initialized = True
                
        # Get the singleton instance
        manager = MyManager(config={'setting': 'value'})
        # Second call returns the same instance
        same_manager = MyManager.get_instance()
        assert manager is same_manager  # True
        ```
    """
    
    # Class variable to store singleton instances
    _instances: ClassVar[Dict[Type['Singleton'], 'Singleton']] = {}

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    @classmethod
    def get_instance(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """Get or create the singleton instance"""
        return cls(*args, **kwargs)
