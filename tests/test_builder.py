"""Tests for MarimoBuilder."""

import json
from pathlib import Path
from sphinx_marimo.builder import MarimoBuilder


def test_generate_manifest(tmp_path):
    """Test that manifest.json is created with correct structure."""
    source_dir = tmp_path / "source"
    build_dir = tmp_path / "build"
    static_dir = tmp_path / "static"

    source_dir.mkdir()
    build_dir.mkdir()
    static_dir.mkdir()

    builder = MarimoBuilder(source_dir, build_dir, static_dir)
    builder.notebooks = [
        {
            "name": "example1",
            "path": "example1.py",
            "output": "notebooks/example1.html",
        },
        {
            "name": "example2",
            "path": "example2.py",
            "output": "notebooks/example2.html",
        },
    ]

    builder._generate_manifest()

    manifest_file = static_dir / "manifest.json"
    assert manifest_file.exists()

    manifest = json.loads(manifest_file.read_text())
    assert "notebooks" in manifest
    assert "version" in manifest
    assert len(manifest["notebooks"]) == 2
    assert manifest["notebooks"][0]["name"] == "example1"
    assert manifest["notebooks"][1]["name"] == "example2"


def test_create_placeholder(tmp_path):
    """Test that placeholder HTML is created with correct content."""
    source_dir = tmp_path / "source"
    build_dir = tmp_path / "build"
    static_dir = tmp_path / "static"

    source_dir.mkdir()
    build_dir.mkdir()
    static_dir.mkdir()

    builder = MarimoBuilder(source_dir, build_dir, static_dir)
    output_path = tmp_path / "placeholder.html"
    source_path = Path("notebooks/example.py")

    builder._create_placeholder(output_path, source_path)

    assert output_path.exists()
    content = output_path.read_text()

    assert "<!DOCTYPE html>" in content
    assert "Marimo Notebook" in content
    assert str(source_path) in content
    assert "install marimo" in content


def test_create_runtime_placeholder(tmp_path):
    """Test that runtime placeholder JS is created."""
    source_dir = tmp_path / "source"
    build_dir = tmp_path / "build"
    static_dir = tmp_path / "static"
    runtime_dir = tmp_path / "runtime"

    source_dir.mkdir()
    build_dir.mkdir()
    static_dir.mkdir()
    runtime_dir.mkdir()

    builder = MarimoBuilder(source_dir, build_dir, static_dir)
    builder._create_runtime_placeholder(runtime_dir)

    js_file = runtime_dir / "marimo-wasm.js"
    assert js_file.exists()

    content = js_file.read_text()
    assert "window.MarimoRuntime" in content
    assert "init: function" in content
