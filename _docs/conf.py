# Configuration file for the Sphinx documentation builder.

import os
import sys
import sphinx_gallery
sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------
project = 'Sphinx-Marimo'
copyright = '2025'
author = 'Vincent D. Warmerdam'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx_gallery.gen_gallery',  # Must come before sphinx_marimo for proper integration
    'jupyterlite_sphinx',
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
    'jupyterlite': {
        'use_jupyter_lab': False
    }
}

# -- JupyterLite configuration ----------------------------------------------
jupyterlite_contents = ["./jupyterlite_contents/auto_examples"]

html_theme_options = {
    "navbar_center": ["navbar-nav"],
    "show_toc_level": 2,
    "logo": {
        "text": "🖼️ Sphinx-Gallery",
    },
    "github_url": "https://github.com/sphinx-gallery/sphinx-gallery",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/sphinx-gallery",
            "icon": "fa-solid fa-box",
        },
    ],
    "secondary_sidebar_items": ["page-toc", "sg_download_links", "sg_launcher_links"],
    "jupyterlite": {
        "notebook_modification_function": "sg_doc_build.notebook_modification_function",
    },
}

# -- Marimo Gallery integration ---------------------------------------------
marimo_gallery_button_text = 'launch marimo'
# Control which buttons to show on Gallery pages
marimo_show_footer_button = True   # Show download button in page footer
marimo_show_sidebar_button = True  # Show launch button in right sidebar