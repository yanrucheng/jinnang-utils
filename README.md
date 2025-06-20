# Jinnang Utils

A comprehensive collection of Python utility functions and classes for common programming tasks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

## Overview

Jinnang Utils is a utility library that provides a set of reusable functions and classes to simplify common programming tasks. The package is designed to be lightweight, efficient, and easy to use.

## Features

- **Hash Utilities**: Create stable hashes for objects, calculate MD5 hashes, and generate partial file hashes
- **File Operations**: Validate folder names and file captions
- **System Utilities**: Suppress stdout/stderr for cleaner output
- **Formatting Tools**: Safe string formatting and token calculation
- **Debugging Helpers**: Get Python execution info and class information
- **Arithmetic Functions**: Statistical operations like finding the mode
- **Common Patterns**: Design patterns, decorators, and formatters

## Installation

```bash
pip install jinnang-utils
```

## Usage

### Hash Utilities

```python
from jinnang import hash

# Create a stable hash for any object
hash_value = hash.stable_hash({"key": "value"})
print(hash_value)  # Outputs a consistent MD5 hash

# Calculate MD5 hash
md5_hash = hash.md5("string to hash")

# Generate partial file hash
file_hash = hash.partial_file_hash("path/to/file")
```

### File Operations

```python
from jinnang import file

# Check if a folder name is valid
if file.is_bad_folder_name("folder/with/invalid:chars"):
    print("Invalid folder name")

# Check if a caption has too many question marks
if file.is_bad_llm_caption("Is this a question? Or this? Or maybe this? Or this one too?"):
    print("Too many questions in caption")
```

### System Utilities

```python
from jinnang import system

# Suppress stdout and stderr
with system.suppress_stdout_stderr():
    print("This will not be displayed")
    
# Suppress only C-level stdout
with system.suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
    # Code that generates C-level output
    pass
```

### Formatting Tools

```python
from jinnang import formatting
from jinnang.common import TruncatedPrettyPrinter, ResolutionPreset, Verbosity

# Calculate tokens for image dimensions
tokens = formatting.calculate_tokens(width=512, height=512)

# Safe string formatting
result = formatting.safe_format("Hello {name}", {"name": "World", "age": 30})

# Use truncated pretty printer
printer = TruncatedPrettyPrinter(max_width=80)
printer.pprint(large_object)
```

### Debugging Helpers

```python
from jinnang import debug

# Get Python execution information
exec_info = debug.get_python_execution_info()
print(exec_info["version"])

# Get class information
class_info = debug.get_class_info(MyClass)
print(class_info)

# Print execution information
debug.print_execution_info()

# Print class information
debug.print_class_info(MyClass)
```

### Arithmetic Functions

```python
from jinnang import arithmetic

# Find the mode of a list
mode = arithmetic.get_mode([1, 2, 2, 3, 3, 3, 4])
print(mode)  # Outputs: 3
```

### Common Patterns

```python
from jinnang.common import mock_when, fail_recover, custom_retry, BadInputException

# Use decorators
@mock_when(condition=lambda: is_test_environment)
def function_to_mock():
    # Real implementation
    pass

@fail_recover(default_value=None)
def function_that_might_fail():
    # Implementation that might raise exceptions
    pass

@custom_retry(max_attempts=3, delay=1)
def function_to_retry():
    # Implementation that might need retrying
    pass

# Use exceptions
raise BadInputException("Invalid input provided")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.