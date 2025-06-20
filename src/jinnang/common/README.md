# Jinnang Common Module

This module provides reusable class definitions for the jinnang utility package.

## Modules

- `patterns.py`: Design pattern implementations (Singleton, Factory, etc.)
- `formatters.py`: Data formatting and display utilities

## Usage

Classes can be imported directly from the jinnang.common module:

```python
from jinnang.common import TruncatedPrettyPrinter, ResolutionPreset, Verbosity, GenericSingletonFactory
```

Or from their specific modules:

```python
from jinnang.common.formatters import TruncatedPrettyPrinter
from jinnang.common.patterns import GenericSingletonFactory
```

This directory contains reusable class definitions that provide common patterns and formatting utilities used throughout the jinnang package and its consumers.

## Overview

The common module is organized into logical files based on functionality:

- **patterns.py**: Implementation of design patterns (Singleton, Factory, etc.)
- **formatters.py**: Data formatting and display utilities

## Available Classes

### Pattern Classes

- `GenericSingletonFactory`: A base class implementing the Singleton pattern with a factory method approach, ensuring only one instance of a class exists and providing a standardized way to access it.

### Formatting Classes

- `ResolutionPreset`: An enumeration of standard video resolution presets with exact dimensions, supporting comparison operations.
- `Verbosity`: An enumeration for controlling output verbosity levels throughout the application.
- `TruncatedPrettyPrinter`: An enhanced pretty printer that truncates long collections, showing only a subset of items from the beginning and end.

## Usage Examples

### GenericSingletonFactory

```python
from jinnang.common import GenericSingletonFactory

class MyManager(GenericSingletonFactory):
    def __init__(self, config=None):
        self.config = config or {}
        
# Get the singleton instance
manager = MyManager.get_instance(config={'setting': 'value'})
# Second call returns the same instance
same_manager = MyManager.get_instance()
assert manager is same_manager  # True
```

### TruncatedPrettyPrinter

```python
from jinnang.common import TruncatedPrettyPrinter

# Create a printer that shows 4 items at start/end of large collections
printer = TruncatedPrettyPrinter(show_num=4)

# Print a large list with truncation
large_list = list(range(100))
printer.pprint(large_list)
# Output will show first 2 and last 2 items with count of omitted items
```

### ResolutionPreset

```python
from jinnang.common import ResolutionPreset

# Compare resolutions
if ResolutionPreset.RES_720P > ResolutionPreset.RES_480P:
    print("720p is higher resolution than 480p")
    
# Get dimensions
width, height = ResolutionPreset.RES_1080P.value
print(f"1080p resolution: {width}x{height}")
```