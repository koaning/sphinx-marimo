# Sphinx Gallery Integration

The sphinx-marimo extension now supports integration with Sphinx Gallery! This allows you to add "launch marimo" buttons alongside existing Binder/JupyterLite buttons on Gallery-generated example pages.

## How It Works

1. **Sphinx Gallery** converts Python scripts to HTML documentation and generates `.ipynb` notebook files
2. **sphinx-marimo** detects Gallery's presence and converts the `.ipynb` files to Marimo WASM notebooks
3. **Gallery buttons** automatically include a "launch marimo" button that opens the interactive notebook

## Setup

### 1. Install Dependencies

```bash
uv add sphinx-gallery sphinx-marimo marimo
```

### 2. Configure Sphinx Gallery + Marimo in conf.py

```python
# Standard Sphinx Gallery configuration
extensions = [
    'sphinx_gallery.gen_gallery',  # Must come before sphinx_marimo
    'sphinx_marimo',
    # ... other extensions
]

# Configure Sphinx Gallery
sphinx_gallery_conf = {
    'examples_dirs': '../examples',   # Path to example scripts
    'gallery_dirs': 'auto_examples',  # Output directory
    'filename_pattern': '/plot_.*\.py$',
}

# Configure Marimo launcher (optional)
marimo_gallery_button_text = 'launch marimo'  # Button text (default: "launch marimo")
```

### 3. Create Gallery Examples

Create Python scripts in your `examples/` directory with Gallery format:

```python
# examples/plot_basic_example.py
"""
Basic Interactive Example
=========================

This example demonstrates basic interactivity with sliders and plots.
"""

import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Interactive Sine Wave')
plt.grid(True)
plt.show()
```

### 4. Build Documentation

```bash
sphinx-build -b html docs docs/_build
```

## What Happens During Build

1. **Sphinx Gallery phase**:
   - Finds `examples/plot_*.py` files
   - Executes them and captures output
   - Generates `.rst` documentation files
   - Creates `.ipynb` notebook versions in `notebooks/auto_examples/`

2. **Marimo integration phase**:
   - Detects Gallery's generated `.ipynb` files
   - Converts each `.ipynb` → Marimo format → WASM notebook
   - Places WASM notebooks in `_static/marimo/gallery/`
   - Injects launcher buttons into Gallery pages

3. **Final result**:
   - Gallery example pages now have red "launch marimo" buttons
   - Clicking opens the interactive Marimo notebook in a new tab
   - Works alongside existing Binder/JupyterLite buttons

## Button Styling

The launcher buttons automatically match Sphinx Gallery's button style:
- Red background (#dc3545) matching Binder button color
- Hover effects and responsive design
- Dark mode support
- Integrates seamlessly with existing Gallery button groups

## Configuration Options

```python
# In conf.py
marimo_gallery_button_text = 'open in marimo'  # Customize button text
```

## File Structure After Build

```
docs/
├── auto_examples/           # Gallery-generated HTML pages
├── notebooks/
│   └── auto_examples/       # Gallery-generated .ipynb files
├── _static/
│   └── marimo/
│       ├── gallery/         # Our Marimo WASM notebooks
│       │   ├── plot_basic_example.html
│       │   └── gallery_manifest.json
│       ├── gallery-launcher.css
│       └── gallery-launcher.js
```

## Compatibility

- ✅ Works with Sphinx Gallery 0.10+
- ✅ Compatible with Binder integration
- ✅ Compatible with JupyterLite integration
- ✅ Supports all major Sphinx themes
- ✅ Mobile responsive design

The integration is automatic - no changes needed to existing Gallery examples!