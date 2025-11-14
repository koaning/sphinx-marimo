Examples
========

This page demonstrates various ways to embed Marimo notebooks in your documentation.

Basic Example
-------------

A simple interactive notebook with UI components. This uses the default click-to-load behavior:

.. marimo:: example.py
   :height: 700px
   :load-button-text: Click to load interactive demo

Data Analysis Example
---------------------

A more complex notebook showing data analysis capabilities with click-to-load disabled for immediate interaction:

.. marimo:: data_analysis.py
   :height: 800px
   :width: 100%
   :click-to-load: false

Configuration
-------------

To use sphinx-marimo in your documentation, add it to your ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinx_marimo',
   ]

   # Marimo configuration
   marimo_notebook_dir = '../notebooks'      # Where your notebooks are located
   marimo_build_dir = '_build/marimo'        # Temporary build directory
   marimo_output_dir = '_static/marimo'      # Output directory for built notebooks
   marimo_default_height = '600px'           # Default iframe height
   marimo_default_width = '100%'             # Default iframe width

   # Parallel build and caching
   marimo_parallel_build = True              # Enable parallel notebook building
   marimo_n_jobs = -1                        # Number of parallel jobs (-1 = auto-detect CPU cores)
   marimo_cache_notebooks = True             # Enable caching to speed up repeated builds

   # Click-to-load configuration
   marimo_click_to_load = True               # Enable click-to-load for better performance
   marimo_load_button_text = 'Load Interactive Notebook'  # Button text

Directive Options
-----------------

The ``marimo`` directive supports several options:

* ``height``: Set the iframe height (default: 600px)
* ``width``: Set the iframe width (default: 100%)
* ``click-to-load``: Override global click-to-load setting (true/false)
* ``load-button-text``: Custom text for the load button

Example:

.. code-block:: rst

   .. marimo:: notebook.py
      :height: 800px
      :width: 90%

   # Force immediate loading for this notebook
   .. marimo:: quick_demo.py
      :click-to-load: false

   # Force click-to-load with custom button text
   .. marimo:: expensive_analysis.py
      :click-to-load: true
      :load-button-text: Start Analysis

Tips for Creating Notebooks
----------------------------

1. **Keep notebooks focused**: Each notebook should demonstrate a specific concept
2. **Use interactive elements**: Take advantage of Marimo's UI components
3. **Optimize for web**: Consider load time and performance
4. **Test locally**: Use ``marimo run`` to test notebooks before building docs

Building Documentation
----------------------

To build the documentation with embedded notebooks:

.. code-block:: bash

   # Using just
   just build-docs

   # Or using Sphinx directly
   sphinx-build -b html _docs docs

The build process will:

1. Discover all Marimo notebooks in the configured directory
2. Build each notebook to WASM format
3. Copy notebooks and runtime to static directory
4. Generate the documentation with embedded iframes