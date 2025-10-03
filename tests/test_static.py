"""Tests for static file generation."""

from pathlib import Path
from sphinx_marimo.static import (
    create_marimo_css,
    create_marimo_loader_js,
    create_gallery_launcher_css,
    create_gallery_launcher_js,
)


def test_create_marimo_css(tmp_path):
    """Test that marimo CSS file is created with expected content."""
    create_marimo_css(tmp_path)

    css_file = tmp_path / "marimo-embed.css"
    assert css_file.exists()

    content = css_file.read_text()
    assert ".marimo-embed" in content
    assert ".marimo-loading" in content
    assert ".marimo-error" in content
    assert "animation: marimo-spin" in content


def test_create_marimo_loader_js(tmp_path):
    """Test that marimo loader JS file is created with expected content."""
    create_marimo_loader_js(tmp_path)

    js_file = tmp_path / "marimo-loader.js"
    assert js_file.exists()

    content = js_file.read_text()
    assert "window.MarimoLoader" in content
    assert "loadedNotebooks" in content
    assert "load: function" in content
    assert "initializeNotebook" in content


def test_create_gallery_launcher_css(tmp_path):
    """Test that gallery launcher CSS file is created with expected content."""
    create_gallery_launcher_css(tmp_path)

    css_file = tmp_path / "gallery-launcher.css"
    assert css_file.exists()

    content = css_file.read_text()
    assert ".marimo-gallery-launcher" in content
    assert ".marimo-sidebar-button" in content
    assert "background-color" in content


def test_create_gallery_launcher_js(tmp_path):
    """Test that gallery launcher JS file is created with expected content."""
    create_gallery_launcher_js(tmp_path)

    js_file = tmp_path / "gallery-launcher.js"
    assert js_file.exists()

    content = js_file.read_text()
    assert "window.MarimoGalleryLauncher" in content
    assert "inject: function" in content
    assert "addMarimoButton" in content
    assert "addMarimoSidebarButton" in content
    assert "extractNotebookName" in content
