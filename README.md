# sphinx-marimo

A Sphinx extension for embedding interactive Marimo notebooks in documentation with WASM support, similar to Jupyter-Lite.

## Installation

Using `uv` (recommended):

```bash
uv add sphinx-marimo
```

Or using `pip`:

```bash
pip install sphinx-marimo
```

## Quick Start

1. Add the extension to your `conf.py`:

```python
extensions = [
    'sphinx_marimo',
    # ... other extensions
]

# Optional configuration
marimo_notebook_dir = 'notebooks'  # Directory containing .py Marimo notebooks
marimo_default_height = '600px'
marimo_default_width = '100%'
```

2. Create a Marimo notebook (`.py` file):

```python
import marimo

__generated_with = "0.1.0"
app = marimo.App()

@app.cell
def __():
    import marimo as mo
    return mo,

@app.cell
def __(mo):
    slider = mo.ui.slider(1, 10, value=5)
    mo.md(f"Value: {slider.value}")
    return slider,
```

3. Embed it in your documentation:

```rst
.. marimo:: path/to/notebook.py
   :height: 800px
   :width: 100%
```

## Sphinx Gallery Integration

The extension automatically detects Sphinx Gallery and adds "launch marimo" buttons:

```python
# In conf.py
extensions = [
    'sphinx_gallery.gen_gallery',  # Must come before sphinx_marimo
    'sphinx_marimo',
]

sphinx_gallery_conf = {
    'examples_dirs': '../gallery_examples',
    'gallery_dirs': 'auto_examples',
}

# Control button visibility
marimo_show_footer_button = True
marimo_show_sidebar_button = True

# Transform converted notebooks (optional)
marimo_prepend_markdown = """
⚠️ **Note**: This notebook was automatically converted from Jupyter.
"""
marimo_move_imports_to_top = True  # Ensure imports run first
```

Gallery examples will automatically include "launch marimo" buttons alongside existing Binder/JupyterLite buttons.

## Architecture

The extension works by:

1. **Build Phase**: Converting Marimo `.py` notebooks to WASM during Sphinx build
2. **Runtime**: Serving notebooks as static files that run in the browser
3. **Gallery Integration**: Converting Gallery-generated `.ipynb` files to Marimo WASM
4. **UI Integration**: Injecting launcher buttons into Gallery pages

## Examples

See the [documentation](https://your-docs-url.com) for live examples and full usage guide.

## Requirements

- Python 3.8+
- Sphinx 4.0+
- Marimo 0.1.0+
- For Gallery integration: sphinx-gallery 0.10+

## Development

```bash
git clone https://github.com/your-repo/sphinx-marimo
cd sphinx-marimo
uv venv
uv pip install -e .
```

## License

MIT License - see LICENSE file for details.