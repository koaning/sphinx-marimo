# sphinx-marimo

A Sphinx extension for embedding interactive Marimo notebooks in documentation with WASM support, similar to Jupyter-Lite.

## Features

- ✨ **Zero-config WASM deployment** - Notebooks run entirely in the browser
- ✨ **Seamless Sphinx integration** - Works with any Sphinx theme
- 🚀 **Interactive notebooks** - Full Marimo interactivity in your docs
- 🚀 **Build-time compilation** - Notebooks are compiled to WASM during docs build
- ✨ **Static site compatible** - Works with GitHub Pages, Read the Docs, etc.
- 🎨 **Sphinx Gallery integration** - Automatically adds "launch marimo" buttons to Gallery examples

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

# Customize button text (optional)
marimo_gallery_button_text = 'launch marimo'
```

Gallery examples will automatically include red "launch marimo" buttons alongside existing Binder/JupyterLite buttons.

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