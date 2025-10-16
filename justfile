# Build documentation and prepare for GitHub Pages
build-docs:
    # Build the documentation with Sphinx (source in _docs, output to docs for GitHub Pages)
    cd _docs && uv run sphinx-build -b html . ../docs
    # Ensure no Jekyll processing
    touch docs/.nojekyll
    echo "Documentation built from _docs/ to docs/ for GitHub Pages"

# Clean build artifacts
clean:
    rm -rf _docs/_build/
    rm -rf docs/*
    rm -rf docs/_build/.marimo_cache
    echo "Cleaned build artifacts and cache"

# Development server (if you want to test locally)
serve:
    uv run python -m http.server 1234 --directory docs

# Run tests
test:
    uv run pytest tests/ -v

# Full rebuild
rebuild: clean build-docs

pypi:
    uv build
    uv publish
