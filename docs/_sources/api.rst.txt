API Reference
=============

This page documents the Sphinx-Marimo extension API.

Extension Setup
---------------

.. py:function:: sphinx_marimo.setup(app)

   Main setup function for the Sphinx extension.

   :param app: Sphinx application instance
   :type app: sphinx.application.Sphinx
   :returns: Extension metadata dictionary
   :rtype: dict

   This function is called by Sphinx during initialization. It registers:

   * Configuration values
   * The ``marimo`` directive
   * Event handlers for building notebooks
   * Static CSS and JavaScript files

Configuration Values
--------------------

The following configuration values can be set in ``conf.py``:

.. py:data:: marimo_notebook_dir

   Directory containing Marimo notebook files (relative to source directory).

   :type: str
   :default: "notebooks"

.. py:data:: marimo_build_dir

   Directory for build artifacts (relative to output directory).

   :type: str
   :default: "_build/marimo"

.. py:data:: marimo_output_dir

   Directory for static files (relative to output directory).

   :type: str
   :default: "_static/marimo"

.. py:data:: marimo_default_height

   Default height for embedded notebooks.

   :type: str
   :default: "600px"

.. py:data:: marimo_default_width

   Default width for embedded notebooks.

   :type: str
   :default: "100%"

Directive
---------

.. rst:directive:: .. marimo:: notebook_path

   Embed a Marimo notebook in the documentation.

   :param notebook_path: Path to the notebook file (relative to ``marimo_notebook_dir``)
   :type notebook_path: str

   **Options:**

   .. rst:directive:option:: height
      :type: string

      Height of the embedded iframe (e.g., "700px", "80vh")

   .. rst:directive:option:: width
      :type: string

      Width of the embedded iframe (e.g., "100%", "800px")

   .. rst:directive:option:: class
      :type: string

      Additional CSS classes to apply to the container

   .. rst:directive:option:: theme
      :type: string

      Theme for the notebook ("light", "dark", or "auto")

   **Example:**

   .. code-block:: rst

      .. marimo:: examples/my_notebook.py
         :height: 800px
         :width: 90%
         :theme: dark