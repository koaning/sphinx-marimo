Welcome to Sphinx-Marimo Documentation
=======================================

This documentation demonstrates the Sphinx-Marimo extension, which allows you to embed
interactive Marimo notebooks directly in your Sphinx documentation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   gallery
   api

Introduction
------------

Sphinx-Marimo enables you to include Marimo notebooks in your documentation with WASM support,
similar to how Jupyter-Lite works. This means your notebooks run entirely in the browser without
requiring a server.

Quick Example
-------------

Here's a simple Marimo notebook embedded in the documentation:

.. marimo:: example.py
   :height: 700px
   :width: 100%

Features
--------

* **Zero-config WASM deployment**: Notebooks are automatically built to WASM during documentation build
* **Interactive notebooks**: Full Marimo interactivity in your documentation
* **Static site compatible**: Works with GitHub Pages, Read the Docs, and other static hosts
* **Customizable embedding**: Control size, theme, and styling of embedded notebooks
* **Sphinx Gallery integration**: Automatically adds "launch marimo" buttons to Gallery examples

Installation
------------

Install the extension using pip or uv:

.. code-block:: bash

   pip install sphinx-marimo

Or with uv:

.. code-block:: bash

   uv add sphinx-marimo

Configuration
-------------

Add the extension to your ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinx_marimo',
       # ... other extensions
   ]

   # Optional configuration
   marimo_notebook_dir = 'notebooks'  # Directory containing .py Marimo notebooks
   marimo_default_height = '600px'
   marimo_default_width = '100%'

Usage
-----

Use the ``marimo`` directive in your RST files:

.. code-block:: rst

   .. marimo:: path/to/notebook.py
      :height: 800px
      :width: 100%
      :theme: light

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`