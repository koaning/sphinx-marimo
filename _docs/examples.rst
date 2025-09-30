Examples
========

This page demonstrates various ways to embed Marimo notebooks in your documentation.

Basic Example
-------------

A simple interactive notebook with UI components:

.. marimo:: example.py
   :height: 700px

Data Analysis Example
---------------------

A more complex notebook showing data analysis capabilities:

.. marimo:: data_analysis.py
   :height: 800px
   :width: 100%

Configuration
-------------

To use sphinx-marimo in your documentation, add it to your ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinx_gallery.gen_gallery',  # Must come before sphinx_marimo
       'sphinx_marimo',
   ]

   # Marimo configuration
   marimo_notebook_dir = '../notebooks'      # Where your notebooks are located
   marimo_build_dir = '_build/marimo'        # Temporary build directory
   marimo_output_dir = '_static/marimo'      # Output directory for built notebooks
   marimo_default_height = '600px'           # Default iframe height
   marimo_default_width = '100%'             # Default iframe width

   # Sphinx Gallery integration
   sphinx_gallery_conf = {
       'examples_dirs': '../gallery_examples',
       'gallery_dirs': 'auto_examples',
       'filename_pattern': r'/plot_.*\.py$',
   }

   # Marimo Gallery integration
   marimo_gallery_button_text = 'launch marimo'  # Button text in gallery examples

Directive Options
-----------------

The ``marimo`` directive supports several options:

* ``height``: Set the iframe height (default: 600px)
* ``width``: Set the iframe width (default: 100%)

Example:

.. code-block:: rst

   .. marimo:: notebook.py
      :height: 800px
      :width: 90%

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