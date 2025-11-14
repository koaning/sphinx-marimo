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

## Click-to-Load Feature

Marimo notebooks use WASM which can be compute-intensive. By default, notebooks only load when clicked to improve performance:

```python
# In conf.py
marimo_click_to_load = True  # Enable click-to-load (default)
marimo_load_button_text = "Load Interactive Notebook"  # Customize button text
```

When `marimo_click_to_load` is enabled:
- Notebooks show a "Load Interactive Notebook" button instead of loading immediately
- Users click the button to start loading the WASM notebook
- This significantly improves page load times, especially on mobile devices
- Reduces bandwidth usage for users who don't interact with every notebook

To disable click-to-load and revert to immediate loading:

```python
marimo_click_to_load = False
```

## Architecture

The extension works by:

1. **Build Phase**: Converting Marimo `.py` notebooks to WASM during Sphinx build
2. **Runtime**: Serving notebooks as static files that run in the browser
3. **Click-to-Load**: Deferring notebook loading until user interaction for better performance

## Examples

See the [documentation](https://your-docs-url.com) for live examples and full usage guide.

## Requirements

- Python 3.8+
- Sphinx 4.0+
- Marimo 0.1.0+

## Development

```bash
git clone https://github.com/your-repo/sphinx-marimo
cd sphinx-marimo
uv venv
uv pip install -e .
```

## License

MIT License - see LICENSE file for details.