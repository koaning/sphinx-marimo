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

Marimo notebooks use WASM which can be compute-intensive. The extension offers multiple loading modes to optimize performance and user experience:

### Loading Modes

```python
# In conf.py
marimo_click_to_load = True  # Can be: False, True/"overlay", or "compact"
marimo_load_button_text = "Load Interactive Notebook"  # Customize button text
```

#### Available Modes:

1. **Immediate Loading** (`False`) - Traditional behavior, notebooks load immediately
2. **Overlay Mode** (`True` or `"overlay"`) - Full-height overlay with centered button (default)
3. **Compact Mode** (`"compact"`) - Space-saving button that expands when clicked

### Per-Notebook Configuration

Override the global setting for individual notebooks:

```rst
# Compact mode - saves screen space
.. marimo:: heavy_computation.py
   :click-to-load: compact
   :load-button-text: Run Analysis

# Overlay mode - full height with centered button
.. marimo:: demo.py
   :click-to-load: overlay
   :load-button-text: Start Demo

# Immediate loading - no button
.. marimo:: quick_example.py
   :click-to-load: false
```

### Use Cases:

- **Compact mode**: Perfect for documentation with multiple notebooks on one page
- **Overlay mode**: Best for standalone demos where the notebook is the focus
- **Immediate loading**: Ideal for lightweight, essential notebooks

This flexibility allows you to optimize for:
- Better page load times on mobile devices
- Reduced bandwidth for users who don't interact with every notebook
- Improved user experience with progressive disclosure

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
