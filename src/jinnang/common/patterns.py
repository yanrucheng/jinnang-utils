"""Design pattern implementations for reuse across the jinnang package.

This module provides implementations of common design patterns such as Singleton,
Factory, and other structural patterns that can be reused throughout the application.
"""

import os
from typing import TypeVar, Type, Dict, Any, Optional, List, ClassVar

# Type variable for generic class methods
T = TypeVar('T')

class GenericSingletonFactory:
    """
    Generic singleton factory base class compatible with Python 3.8+.
    
    This class implements the Singleton pattern with a factory method approach,
    ensuring only one instance of a class exists and providing a standardized
    way to access it. It's designed to be subclassed by concrete singleton classes.
    
    Example:
        ```python
        class MyManager(GenericSingletonFactory):
            def __init__(self, config=None):
                self.config = config or {}
                
        # Get the singleton instance
        manager = MyManager.get_instance(config={'setting': 'value'})
        # Second call returns the same instance
        same_manager = MyManager.get_instance()
        assert manager is same_manager  # True
        ```
    """
    
    # Class variable to store singleton instances
    _instances: ClassVar[Dict[Type['GenericSingletonFactory'], 'GenericSingletonFactory']] = {}
    
    @classmethod
    def get_instance(cls: Type[T], *args, **kwargs) -> T:
        """Get or create the singleton instance"""
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]
    
    @staticmethod
    def resolve_file_path(
        explicit_path: Optional[str] = None,
        filename: str = "",
        search_locations: Optional[List[str]] = None,
        caller_module_path: Optional[str] = None
    ) -> str:
        """
        Resolve a file path by searching in multiple locations.
        
        This utility method helps locate files by checking multiple directories
        in a predefined order. It's useful for configuration files, templates,
        or other resources that might be in different locations depending on
        the execution context.
        
        Args:
            explicit_path: Direct file path to check first
            filename: Name of the file to find
            search_locations: List of directories to search in
            caller_module_path: Path to the caller's module (__file__). If None, uses this module's path.
            
        Returns:
            str: Absolute path to the found file
            
        Raises:
            FileNotFoundError: If the file cannot be found in any location
        """
        if explicit_path and os.path.exists(explicit_path):
            return explicit_path
            
        # Use caller's module path if provided, otherwise use this module's path
        module_path = caller_module_path or __file__
            
        default_locations = [
            '.',  # Current directory
            os.path.dirname(module_path),  # Module directory
            os.path.join(os.path.dirname(module_path), '..'),  # Parent dir
            os.path.join(os.path.dirname(module_path), '../..'),  # Grandparent dir
        ]
        
        locations = search_locations if search_locations is not None else default_locations
        
        for directory in locations:
            potential_path = os.path.join(directory, filename)
            if os.path.exists(potential_path):
                return potential_path
                
        raise FileNotFoundError(
            f"Could not find {filename} in any of these locations: {locations}"
        )