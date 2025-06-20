# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root directory to the path so that Sphinx can find the modules
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'Jinnang Utils'
copyright = '2023, Cheng Yanru'
author = 'Cheng Yanru'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Extension configurations
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}