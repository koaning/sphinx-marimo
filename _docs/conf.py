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

# Parallel build and caching (default values shown)
marimo_parallel_build = True    # Enable parallel notebook building
marimo_n_jobs = -1               # Number of parallel jobs (-1 = auto-detect CPU cores)
marimo_cache_notebooks = True    # Enable caching to speed up repeated builds

# Click-to-load configuration
marimo_click_to_load = True           # Options: False, True/"overlay", "compact"
marimo_load_button_text = "Load Interactive Notebook"

html_theme_options = {
    "navbar_center": ["navbar-nav"],
    "show_toc_level": 2,
    "logo": {
        "text": "📊 Sphinx-Marimo",
    },
    "github_url": "https://github.com/koaning/sphinx-marimo",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/sphinx-marimo",
            "icon": "fa-solid fa-box",
        },
    ],
    "secondary_sidebar_items": ["page-toc"],
}