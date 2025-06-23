#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Remove the dist directory if it exists
if [ -d "dist" ]; then
  rm -r dist
fi

# Build the package
python3 -m build

# Upload the package to PyPI
python3 -m twine upload dist/*