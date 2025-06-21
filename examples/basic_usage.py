#!/usr/bin/env python3
"""
Basic usage examples for the jinnang-utils package.

This script demonstrates how to use various utilities provided by the jinnang package.
"""

# Import the jinnang package
from jinnang import hash, file, system, formatting, debug, arithmetic
from jinnang.common.verbosity import Verbosity
from jinnang.media.resolution import ResolutionPreset

# Example 1: Using hash utilities
print("\n=== Hash Utilities ===\n")

# Create a stable hash for a dictionary
data = {"name": "John", "age": 30, "city": "New York"}
hash_value = hash.stable_hash(data)
print(f"Stable hash of {data}: {hash_value}")

# Example 2: Using file utilities
print("\n=== File Utilities ===\n")

# Check if a folder name is valid
folder_name = "invalid:folder/name"
if file.is_bad_folder_name(folder_name):
    print(f"'{folder_name}' is not a valid folder name")
else:
    print(f"'{folder_name}' is a valid folder name")

# Check if a caption has too many question marks
caption = "Is this a question? Or this? Or maybe this? Or this one too?"
if file.is_bad_llm_caption(caption):
    print(f"Caption has too many question marks: '{caption}'")
else:
    print(f"Caption is valid: '{caption}'")

# Example 3: Using system utilities
print("\n=== System Utilities ===\n")

# Get Python execution information
exec_info = debug.get_python_execution_info()
print(f"Python version: {exec_info['version_info']}")
print(f"Platform: {exec_info['platform']}")

# Example 4: Using formatting utilities
print("\n=== Formatting Utilities ===\n")

# Calculate tokens for image dimensions
tokens = formatting.calculate_tokens(width=512, height=512)
print(f"Tokens for 512x512 image: {tokens}")

# Safe string formatting
template = "Hello {name}, welcome to {city}"
data = {"name": "Alice", "city": "Wonderland", "extra": "not used"}
formatted = formatting.safe_format(template, data)
print(f"Formatted string: '{formatted}'")

# Example 5: Using arithmetic utilities
print("\n=== Arithmetic Utilities ===\n")

# Find the mode of a list
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
mode = arithmetic.get_mode(numbers)
print(f"Mode of {numbers}: {mode}")

# Example 6: Using pretty printer
print("\n=== Pretty Printer ===\n")

# Create a complex nested structure
complex_data = {
    "users": [
        {"id": 1, "name": "Alice", "roles": ["admin", "user"], "metadata": {"last_login": "2023-01-01"}},
        {"id": 2, "name": "Bob", "roles": ["user"], "metadata": {"last_login": "2023-01-02"}},
        {"id": 3, "name": "Charlie", "roles": ["user", "moderator"], "metadata": {"last_login": "2023-01-03"}},
    ],
    "settings": {
        "theme": "dark",
        "notifications": True,
        "preferences": {"language": "en", "timezone": "UTC", "auto_logout": 30},
    },
}

# Use standard Python pretty printer
import pprint
printer = pprint.PrettyPrinter(max_width=40, compact=True)
print("Pretty printed output:")
printer.pprint(complex_data)

print("\nDone!")