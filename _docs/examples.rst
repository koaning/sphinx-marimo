Examples
========

This page demonstrates various ways to embed Marimo notebooks in your documentation.

Click-to-Load Modes Demo
-------------------------

Compact Mode (Space-Saving)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook uses compact mode - just a small button that expands when clicked:

.. marimo:: example.py
   :height: 700px
   :click-to-load: compact
   :load-button-text: Click to expand and run demo

Overlay Mode (Full Height)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook shows a full-height overlay with a centered button:

.. marimo:: data_analysis.py
   :height: 600px
   :click-to-load: overlay
   :load-button-text: Load Data Analysis

Immediate Loading
~~~~~~~~~~~~~~~~~~

This notebook loads immediately without any button:

.. marimo:: example.py
   :height: 400px
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
* ``click-to-load``: Control loading behavior:

  - ``false`` - Load immediately
  - ``overlay`` - Full-height overlay with button (default)
  - ``compact`` - Small button that expands on click

* ``load-button-text``: Custom text for the load button

Examples:

.. code-block:: rst

   # Compact mode - saves screen space
   .. marimo:: notebook1.py
      :height: 800px
      :click-to-load: compact
      :load-button-text: Expand to run notebook

   # Overlay mode - shows button in center
   .. marimo:: notebook2.py
      :height: 600px
      :click-to-load: overlay
      :load-button-text: Load Interactive Demo

   # Immediate loading - no button
   .. marimo:: notebook3.py
      :height: 400px
      :click-to-load: false

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