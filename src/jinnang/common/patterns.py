"""Design pattern implementations for reuse across the jinnang package.

This module provides implementations of common design patterns such as Singleton,
Factory, and other structural patterns that can be reused throughout the application.
"""

import os
from typing import TypeVar, Type, Dict, Any, Optional, List, ClassVar

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


class SingletonFileLoader(Singleton):
    """
    Singleton class with file loading capabilities.
    
    This class combines the Singleton pattern with file path resolution,
    allowing subclasses to automatically load files during initialization.
    
    Example:
        ```python
        class ConfigManager(SingletonFileLoader):
            def __init__(self, filename=None, caller_module_path=None, **kwargs):
                super().__init__(filename, caller_module_path, **kwargs)
                if not hasattr(self, '_config_initialized'):
                    # Load configuration from file
                    self._config_initialized = True
                
        # Both ways work identically
        config = ConfigManager('config.json', caller_module_path=__file__)
        same_config = ConfigManager.get_instance('config.json', caller_module_path=__file__)
        assert config is same_config  # True
        ```
    """

    def __init__(self, filename: Optional[str] = None, caller_module_path: Optional[str] = None, **kwargs: Any):
        if not hasattr(self, '_file_loader_initialized'):
            search_locations = kwargs.pop('search_locations', None)
            if filename:
                try:
                    self.loaded_filepath = self.resolve_file_path(
                        filename=filename,
                        caller_module_path=caller_module_path,
                        search_locations=search_locations
                    )
                except FileNotFoundError:
                    self.loaded_filepath = None
            else:
                self.loaded_filepath = None
            self._file_loader_initialized = True
        super().__init__(**kwargs)
        
    @property
    def filepath(self):
        return self.loaded_filepath

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
