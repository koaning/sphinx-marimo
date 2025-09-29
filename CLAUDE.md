# Claude Code Development Guide

This file contains helpful information for working on the sphinx-marimo project with Claude Code.

## Project Structure

```
sphinx-marimo/
├── src/sphinx_marimo/         # Main package source
│   ├── __init__.py           # Package initialization
│   ├── extension.py          # Main Sphinx extension setup
│   ├── builder.py            # WASM notebook building logic
│   ├── directives.py         # RST directive implementation
│   └── static.py             # Static CSS/JS file management
├── _docs/                    # Sphinx documentation source
│   ├── conf.py              # Sphinx configuration
│   ├── index.rst            # Main documentation page
│   ├── examples.rst         # Examples page
│   └── api.rst              # API reference
├── docs/                     # Built documentation (GitHub Pages)
├── notebooks/                # Example Marimo notebooks
│   ├── example.py           # Basic interactive demo
│   └── data_analysis.py     # Data analysis example
├── pyproject.toml           # Project configuration
├── justfile                 # Build commands
└── README.md               # Project README
```

## Development Setup

1. **Environment Setup**:
   ```bash
   uv venv
   uv pip install -e .
   ```

2. **Build Documentation**:
   ```bash
   just rebuild  # Clean and build docs
   just build-docs  # Just build docs
   just serve    # Serve docs locally at http://localhost:8000
   ```

3. **Key Commands**:
   - `just clean` - Remove build artifacts
   - `just rebuild` - Full clean and rebuild
   - `just serve` - Local development server

## Common Development Tasks

### Adding New Notebook Examples

1. Create a new `.py` file in `notebooks/`
2. Write it as a standard Marimo notebook with `@app.cell` decorators
3. Reference it in documentation using:
   ```rst
   .. marimo:: your_notebook.py
      :height: 700px
      :width: 100%
   ```

### Modifying the Extension

- **Core logic**: Edit `src/sphinx_marimo/extension.py`
- **Build process**: Edit `src/sphinx_marimo/builder.py`
- **Directive behavior**: Edit `src/sphinx_marimo/directives.py`
- **Styling/JS**: Edit `src/sphinx_marimo/static.py`

### Testing Changes

Always run the build process to test changes:
```bash
just rebuild
```

Check the `docs/` directory for the built output, specifically:
- `docs/_static/marimo/notebooks/` - Built WASM notebooks
- `docs/_static/marimo/` - CSS/JS assets
- `docs/index.html` - Main documentation page

### Debugging Build Issues

1. **Notebook build failures**: Check if `marimo export html-wasm` works manually
2. **Extension not loading**: Verify `pyproject.toml` entry points
3. **Static files missing**: Check `setup_static_files()` in `static.py`
4. **Path issues**: Verify `marimo_notebook_dir` configuration

## Architecture Notes

### How the Extension Works

1. **Sphinx Setup** (`extension.py`):
   - Registers the `marimo` directive
   - Configures build event handlers
   - Sets up static file copying

2. **Build Process** (`builder.py`):
   - Scans `notebooks/` directory for `.py` files
   - Runs `marimo export html-wasm` on each notebook
   - Creates manifest of available notebooks
   - Copies Marimo runtime assets

3. **Directive Rendering** (`directives.py`):
   - Processes `.. marimo::` directives in RST files
   - Generates HTML iframe containers
   - Includes initialization JavaScript

4. **Static Assets** (`static.py`):
   - Creates CSS for styling embedded notebooks
   - Creates JavaScript loader for iframe management
   - Handles responsive design and error states

### Key Configuration

In `_docs/conf.py`:
```python
extensions = ['sphinx_marimo']
marimo_notebook_dir = '../notebooks'  # Relative to _docs/
marimo_default_height = '600px'
marimo_default_width = '100%'
```

## Lint and Typecheck Commands

The project uses these development tools:
- `ruff` for linting and formatting
- `mypy` for type checking
- `pytest` for testing

Install dev dependencies:
```bash
uv pip install -e ".[dev]"
```

## GitHub Pages Deployment

The build process outputs to `docs/` which GitHub Pages serves automatically:
- Source files in `_docs/`
- Built files in `docs/` (committed to git)
- `.nojekyll` file prevents Jekyll processing
- WASM notebooks work as static files

## Common Issues

1. **Import errors**: Make sure the virtual environment is activated
2. **Marimo command not found**: Ensure marimo is installed in the environment
3. **404 errors in notebooks**: Check that notebooks built successfully in `docs/_static/marimo/notebooks/`
4. **Styling issues**: Verify CSS files are copied to `docs/_static/marimo/`

## Package Management

This project uses `uv` instead of `pip`:
- `uv add package` to add dependencies
- `uv pip install -e .` for development install
- `uv venv` to create virtual environment