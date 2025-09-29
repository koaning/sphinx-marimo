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

Custom Styling
--------------

You can customize the appearance of embedded notebooks:

.. marimo:: example.py
   :height: 500px
   :width: 80%
   :class: custom-notebook
   :theme: light

Directive Options
-----------------

The ``marimo`` directive supports several options:

* ``height``: Set the iframe height (default: 600px)
* ``width``: Set the iframe width (default: 100%)
* ``class``: Add custom CSS classes
* ``theme``: Set the theme (light/dark/auto)

Example with all options:

.. code-block:: rst

   .. marimo:: notebook.py
      :height: 800px
      :width: 90%
      :class: my-custom-class
      :theme: dark

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

   # Using Sphinx directly
   sphinx-build -b html docs docs/_build

   # Or using Make
   cd docs && make html

The build process will:

1. Discover all Marimo notebooks in the configured directory
2. Build each notebook to WASM format
3. Copy notebooks and runtime to static directory
4. Generate the documentation with embedded iframes