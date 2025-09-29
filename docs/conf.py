# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
project = 'Sphinx-Marimo Example'
copyright = '2024'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx_marimo',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# -- Marimo configuration ----------------------------------------------------
marimo_notebook_dir = '../notebooks'
marimo_build_dir = '_build/marimo'
marimo_output_dir = '_static/marimo'
marimo_default_height = '600px'
marimo_default_width = '100%'