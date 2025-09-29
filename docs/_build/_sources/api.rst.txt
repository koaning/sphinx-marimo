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

Builder Module
--------------

.. py:class:: sphinx_marimo.builder.MarimoBuilder(source_dir, build_dir, static_dir)

   Handles building Marimo notebooks to WASM format.

   :param source_dir: Directory containing source notebooks
   :type source_dir: pathlib.Path
   :param build_dir: Directory for build artifacts
   :type build_dir: pathlib.Path
   :param static_dir: Directory for static output files
   :type static_dir: pathlib.Path

   .. py:method:: build_all_notebooks()

      Build all notebooks found in the source directory.

      This method:

      1. Discovers all ``.py`` files in the source directory
      2. Builds each notebook using ``marimo export html-wasm``
      3. Copies the output to the static directory
      4. Generates a manifest of available notebooks

   .. py:method:: _build_notebook(notebook_path, output_dir)

      Build a single notebook to WASM format.

      :param notebook_path: Path to the notebook file
      :type notebook_path: pathlib.Path
      :param output_dir: Directory for output files
      :type output_dir: pathlib.Path

Static Files
------------

The extension provides two static files:

**marimo-embed.css**
   Styles for embedded notebooks, including:

   * Container styling
   * Loading indicators
   * Error states
   * Responsive design

**marimo-loader.js**
   JavaScript for managing embedded notebooks:

   * Iframe initialization
   * Message passing between parent and iframe
   * Auto-resize functionality
   * Manifest loading

JavaScript API
--------------

.. js:data:: window.MarimoLoader

   Global object for managing Marimo notebooks.

   .. js:function:: load(container, notebookName)

      Load a notebook into a container.

      :param container: DOM element containing the iframe
      :param notebookName: Name of the notebook to load

   .. js:function:: loadManifest()

      Load the notebook manifest from the static directory.

   .. js:function:: initializeNotebook(iframe, notebookName)

      Initialize a loaded notebook iframe.

      :param iframe: The iframe element
      :param notebookName: Name of the notebook

Extending the Extension
------------------------

To extend or customize the extension:

1. **Custom notebook processing**: Override ``MarimoBuilder._build_notebook()``
2. **Additional directives**: Add new directives in the ``setup()`` function
3. **Custom themes**: Modify ``marimo-embed.css``
4. **Advanced features**: Hook into Sphinx events for custom processing

Example of adding a custom configuration:

.. code-block:: python

   def setup(app):
       app.add_config_value('marimo_custom_option', 'default', 'html')
       # ... rest of setup