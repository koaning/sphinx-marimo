"""Integration tests for notebook transformation in the build pipeline."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from sphinx_marimo.gallery_integration import GalleryMarimoIntegration


@pytest.fixture
def mock_sphinx_app(tmp_path):
    """Mock Sphinx app with realistic directory structure."""
    app = Mock()
    app.outdir = str(tmp_path / "build")
    app.srcdir = str(tmp_path / "source")
    Path(app.outdir).mkdir(parents=True)
    Path(app.srcdir).mkdir(parents=True)

    app.config = Mock()
    app.config.extensions = ['sphinx_gallery.gen_gallery']
    app.config.sphinx_gallery_conf = {'gallery_dirs': ['auto_examples']}
    app.config.marimo_parallel_build = False
    app.config.marimo_n_jobs = -1
    app.config.marimo_prepend_markdown = None
    app.config.marimo_move_imports_to_top = False

    return app


@pytest.fixture
def jupyter_notebook_with_out_of_order_imports(tmp_path):
    """Jupyter notebook where imports come after other code."""
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Some computation first\n", "x = 5\n", "y = 10"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Import comes later\n", "import marimo as mo"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["result = x + y"]
            }
        ],
        "metadata": {"nbformat": 4, "nbformat_minor": 4}
    }

    path = tmp_path / "notebook.ipynb"
    path.write_text(json.dumps(notebook))
    return path


def test_gallery_detection_requires_both_extension_and_config(mock_sphinx_app):
    """Gallery should only be detected when both extension and config exist."""
    integration = GalleryMarimoIntegration(mock_sphinx_app)

    # With both: should detect
    assert integration.detect_sphinx_gallery() is True

    # Without extension: should not detect
    mock_sphinx_app.config.extensions = []
    integration2 = GalleryMarimoIntegration(mock_sphinx_app)
    assert integration2.detect_sphinx_gallery() is False

    # Without config: should not detect
    mock_sphinx_app.config.extensions = ['sphinx_gallery.gen_gallery']
    mock_sphinx_app.config.sphinx_gallery_conf = {}
    integration3 = GalleryMarimoIntegration(mock_sphinx_app)
    assert integration3.detect_sphinx_gallery() is False


def test_setup_creates_output_directories(mock_sphinx_app):
    """Setup should create marimo output directory."""
    integration = GalleryMarimoIntegration(mock_sphinx_app)
    integration.gallery_detected = True

    marimo_dir = Path(mock_sphinx_app.outdir) / "_static" / "marimo" / "gallery"
    assert not marimo_dir.exists()

    integration.setup_gallery_directories()

    assert marimo_dir.exists()
    assert integration.marimo_gallery_dir == marimo_dir


def test_config_values_flow_through_to_integration(mock_sphinx_app):
    """Config values should be accessible in integration instance."""
    mock_sphinx_app.config.marimo_prepend_markdown = "Custom warning text"
    mock_sphinx_app.config.marimo_move_imports_to_top = True

    integration = GalleryMarimoIntegration(mock_sphinx_app)

    assert integration.prepend_markdown == "Custom warning text"
    assert integration.move_imports_to_top is True


def test_conversion_pipeline_applies_prepend_markdown(
    jupyter_notebook_with_out_of_order_imports, tmp_path
):
    """Converted notebooks should have prepended markdown when configured."""
    from sphinx_marimo.gallery_integration import _convert_notebook_standalone

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    warning = "⚠️ Automatically converted"

    _, result_path = _convert_notebook_standalone(
        jupyter_notebook_with_out_of_order_imports,
        output_dir,
        memory=None,
        prepend_markdown=warning,
        move_imports_to_top=False,
    )

    # Check intermediate .py file contains the warning
    py_file = output_dir / f"{jupyter_notebook_with_out_of_order_imports.stem}.py"
    py_content = py_file.read_text()

    assert warning in py_content
    # Warning should appear before the original code
    assert py_content.index(warning) < py_content.index("x = 5")


def test_conversion_pipeline_reorders_imports(
    jupyter_notebook_with_out_of_order_imports, tmp_path
):
    """Import cells should move before computation cells."""
    from sphinx_marimo.gallery_integration import _convert_notebook_standalone

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    _, result_path = _convert_notebook_standalone(
        jupyter_notebook_with_out_of_order_imports,
        output_dir,
        memory=None,
        prepend_markdown=None,
        move_imports_to_top=True,
    )

    py_file = output_dir / f"{jupyter_notebook_with_out_of_order_imports.stem}.py"
    py_content = py_file.read_text()

    # Import should come before the computation
    import_pos = py_content.find("import marimo as mo")
    x_pos = py_content.find("x = 5")

    assert import_pos > 0  # Import exists
    assert import_pos < x_pos  # Import comes first


def test_conversion_creates_valid_html_output(
    jupyter_notebook_with_out_of_order_imports, tmp_path
):
    """Conversion should produce an HTML file."""
    from sphinx_marimo.gallery_integration import _convert_notebook_standalone

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    _, result_path = _convert_notebook_standalone(
        jupyter_notebook_with_out_of_order_imports,
        output_dir,
        memory=None,
    )

    assert result_path is not None
    assert result_path.exists()
    assert result_path.suffix == ".html"
    assert result_path.stat().st_size > 0  # Non-empty file


def test_manifest_contains_notebook_mappings(mock_sphinx_app):
    """Gallery manifest should map notebook names to URLs."""
    integration = GalleryMarimoIntegration(mock_sphinx_app)
    integration.gallery_detected = True
    integration.setup_gallery_directories()

    notebooks = {
        "example1": "marimo/gallery/example1.html",
        "example2": "marimo/gallery/example2.html",
    }
    integration._save_gallery_manifest(notebooks)

    manifest_path = integration.marimo_gallery_dir / "gallery_manifest.json"
    manifest = json.loads(manifest_path.read_text())

    assert manifest["total_count"] == 2
    assert manifest["gallery_notebooks"]["example1"] == notebooks["example1"]
    assert manifest["gallery_notebooks"]["example2"] == notebooks["example2"]


def test_launcher_injection_respects_gallery_dirs(mock_sphinx_app):
    """Launcher should only be injected for pages in gallery_dirs."""
    integration = GalleryMarimoIntegration(mock_sphinx_app)
    integration.gallery_detected = True

    # Pages in gallery_dirs should get launcher
    assert integration.should_inject_launcher("auto_examples/plot_foo")
    assert integration.should_inject_launcher("auto_examples/subdir/plot_bar")

    # Other pages should not
    assert not integration.should_inject_launcher("index")
    assert not integration.should_inject_launcher("installation")
    assert not integration.should_inject_launcher("api/functions")


def test_notebook_info_returns_url_for_converted_notebooks(mock_sphinx_app):
    """get_notebook_info should return URLs for notebooks in manifest."""
    integration = GalleryMarimoIntegration(mock_sphinx_app)
    integration.gallery_detected = True
    integration.setup_gallery_directories()

    notebooks = {"plot_scatter": "marimo/gallery/plot_scatter.html"}
    integration._save_gallery_manifest(notebooks)

    # Should find notebook that exists
    info = integration.get_notebook_info("auto_examples/plot_scatter")
    assert info is not None
    assert "plot_scatter" in info["notebook_url"]

    # Should return None for non-existent
    assert integration.get_notebook_info("auto_examples/missing") is None


def test_notebook_info_returns_none_when_gallery_disabled(mock_sphinx_app):
    """get_notebook_info should return None when gallery not detected."""
    integration = GalleryMarimoIntegration(mock_sphinx_app)
    integration.gallery_detected = False

    # Even if we fake a manifest, should return None
    assert integration.get_notebook_info("auto_examples/whatever") is None
