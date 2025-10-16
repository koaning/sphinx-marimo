"""Tests for MarimoBuilder."""

import json
import shutil
import time
from pathlib import Path
import pytest
from sphinx_marimo.builder import MarimoBuilder


@pytest.fixture
def builder_dirs(tmp_path):
    """Fixture providing standard directory structure for MarimoBuilder tests."""
    source_dir = tmp_path / "source"
    build_dir = tmp_path / "build"
    static_dir = tmp_path / "static"

    source_dir.mkdir()
    build_dir.mkdir()
    static_dir.mkdir()

    return source_dir, build_dir, static_dir, tmp_path


def test_generate_manifest(builder_dirs):
    """Test that manifest.json is created with correct structure."""
    source_dir, build_dir, static_dir, tmp_path = builder_dirs

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


def test_create_placeholder(builder_dirs):
    """Test that placeholder HTML is created with correct content."""
    source_dir, build_dir, static_dir, tmp_path = builder_dirs

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


def test_create_runtime_placeholder(builder_dirs):
    """Test that runtime placeholder JS is created."""
    source_dir, build_dir, static_dir, tmp_path = builder_dirs

    runtime_dir = tmp_path / "runtime"
    runtime_dir.mkdir()

    builder = MarimoBuilder(source_dir, build_dir, static_dir)
    builder._create_runtime_placeholder(runtime_dir)

    js_file = runtime_dir / "marimo-wasm.js"
    assert js_file.exists()

    content = js_file.read_text()
    assert "window.MarimoRuntime" in content
    assert "init: function" in content


def test_cache_works(builder_dirs):
    """Test that caching works - second build should use cached result."""
    source_dir, build_dir, static_dir, tmp_path = builder_dirs

    # Create cache directory
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    # Copy a real notebook from the repo
    repo_notebooks = Path(__file__).parent.parent / "notebooks"
    shutil.copy(repo_notebooks / "example.py", source_dir / "example.py")

    # Create builder with caching enabled
    builder = MarimoBuilder(
        source_dir=source_dir,
        build_dir=build_dir,
        static_dir=static_dir,
        cache_dir=cache_dir,
    )

    # First build - should execute marimo export
    start = time.time()
    builder.build_all_notebooks()
    time1 = time.time() - start
    notebooks1 = len(builder.notebooks)

    # Check that cache directory has files
    cache_files = list(cache_dir.rglob("*"))
    assert len(cache_files) > 0, "Cache should have files after first build"

    # Second build - should use cache
    builder.notebooks = []  # Reset
    start = time.time()
    builder.build_all_notebooks()
    time2 = time.time() - start
    notebooks2 = len(builder.notebooks)

    # Both builds should produce same number of notebooks
    assert notebooks1 == notebooks2 == 1, "Both builds should produce same result"

    # Second build should be significantly faster (cached)
    assert time2 < time1, "Second build should be faster (cached)"
