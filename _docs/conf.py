# Configuration file for the Sphinx documentation builder.

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
project = 'Sphinx-Marimo'
copyright = '2025'
author = 'Vincent D. Warmerdam'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx_gallery.gen_gallery',  # Must come before sphinx_marimo for proper integration
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

# -- Sphinx Gallery configuration -------------------------------------------
sphinx_gallery_conf = {
    'examples_dirs': '../gallery_examples',   # Path to gallery example scripts
    'gallery_dirs': 'auto_examples',          # Output directory name
    'filename_pattern': r'/plot_.*\.py$',      # Only process files starting with plot_
    'expected_failing_examples': set(),
    'plot_gallery': 'True',
}

# -- Marimo Gallery integration ---------------------------------------------
marimo_gallery_button_text = 'launch marimo'