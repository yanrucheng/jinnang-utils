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

    def __init__(
        self,
        filename: Optional[str] = None,
        caller_module_path: Optional[str] = None,
        verbosity: Verbosity = Verbosity.FULL,
        **kwargs: Any
    ):
        if not hasattr(self, '_file_loader_initialized'):
            if not (filename or caller_module_path):
                raise ValueError(
                    "At least one of 'filename' or 'caller_module_path' must be provided."
                )

            try:
                self.loaded_filepath = self.resolve_file_path(
                    filename=filename,
                    caller_module_path=caller_module_path,
                    verbosity=verbosity
                )
            except FileNotFoundError:
                self.loaded_filepath = None
            self._file_loader_initialized = True
        super().__init__(**kwargs)
        
    @property
    def filepath(self):
        return self.loaded_filepath

    @staticmethod
    def _get_search_paths(
        filename: str = "",
        caller_module_path: Optional[str] = None,
        verbosity: Verbosity = Verbosity.FULL
    ) -> List[str]:
        """Generates a list of potential file paths based on the caller's module path.

        This static method constructs a prioritized list of absolute file paths
        where a given filename might be located, relative to the calling module.

        Args:
            filename (str): The name of the file to search for.
            caller_module_path (Optional[str]): The `__file__` attribute of the
                calling module, used to determine a relative search path.
            verbosity (Verbosity): The verbosity level for logging.

        Returns:
            List[str]: A list of absolute paths where the file might exist,
            ordered by search priority.
        """
        module_path = caller_module_path or __file__
        locations = [
            os.path.dirname(module_path),
            os.path.join(os.path.dirname(module_path), '..'),
            os.path.join(os.path.dirname(module_path), '../..'),
            '.'
        ]
        potential_paths = [os.path.join(directory, filename) for directory in locations]
        if verbosity >= Verbosity.DETAIL:
            logging.debug(f"Potential search paths for '{filename}': {potential_paths}")
        return potential_paths

    @staticmethod
    def resolve_file_path(
        filename: str = "",
        caller_module_path: Optional[str] = None,
        verbosity: Verbosity = Verbosity.FULL
    ) -> str:
        """Resolves the absolute path to a file based on the caller's module path.

        This static method attempts to find a file by searching through a series
        of prioritized locations relative to the calling module.

        Args:
            filename (str): The name of the file to resolve.
            caller_module_path (Optional[str]): The `__file__` attribute of the
                calling module, used to determine a relative search path.
            verbosity (Verbosity): The verbosity level for logging.

        Returns:
            str: The absolute path to the resolved file.

        Raises:
            FileNotFoundError: If the file cannot be found in any of the specified
                or default search locations.
        """
        if verbosity >= Verbosity.DETAIL:
            logging.debug(f"Searching for filename: {filename}")

        potential_paths = SingletonFileLoader._get_search_paths(
            filename=filename,
            caller_module_path=caller_module_path,
            verbosity=verbosity
        )

        for potential_path in potential_paths:

            if os.path.exists(potential_path) and os.path.isfile(potential_path):
                if verbosity >= Verbosity.ONCE:
                    logging.info(f"Found file: {potential_path}")
                return potential_path

        error_message = f"Could not find {filename} in any of these locations: {potential_paths}"
        if verbosity >= Verbosity.ONCE:
            logging.error(error_message)
        raise FileNotFoundError(error_message)
