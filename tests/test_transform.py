"""Tests for notebook transformation functions."""

from pathlib import Path

import pytest

from sphinx_marimo.transform import (
    move_imports_to_top,
    prepend_markdown,
    transform_notebook,
)


def test_prepend_markdown_adds_content_before_existing_cells():
    """Prepended markdown should appear before existing cells."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    x = 1
    return x,
'''
    result = prepend_markdown(notebook, "Warning text")

    warning_pos = result.find("Warning text")
    x_pos = result.find("x = 1")
    assert 0 < warning_pos < x_pos


def test_move_imports_reorders_cells():
    """Import cells should move to the top, non-import cells stay in original order."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    x = 1
    return x,

@app.cell
def __():
    import marimo as mo
    return mo,

@app.cell
def __():
    y = 2
    return y,
'''
    result = move_imports_to_top(notebook)

    # Positions: import < x < y
    import_pos = result.find("import marimo as mo")
    x_pos = result.find("x = 1")
    y_pos = result.find("y = 2")
    assert import_pos < x_pos < y_pos


def test_move_imports_handles_multiple_imports():
    """All import cells should move to top, preserving their relative order."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    x = 1
    return x,

@app.cell
def __():
    import marimo as mo
    return mo,

@app.cell
def __():
    y = 2
    return y,

@app.cell
def __():
    import marimo
    return marimo,
'''
    result = move_imports_to_top(notebook)

    # Both imports should be before x
    first_import = result.find("import marimo as mo")
    second_import = result.find("import marimo\n    return marimo")
    x_pos = result.find("x = 1")

    assert first_import < x_pos
    assert second_import < x_pos


def test_move_imports_is_noop_when_already_sorted():
    """Should not modify notebooks where imports are already first."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    import marimo as mo
    return mo,

@app.cell
def __():
    x = 1
    return x,
'''
    result = move_imports_to_top(notebook)
    assert result == notebook


def test_transform_notebook_combines_both_operations(tmp_path):
    """Both transformations should apply: warning first, then imports moved, then other cells."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    x = 1
    return x,

@app.cell
def __():
    import marimo as mo
    return mo,
'''
    nb_path = tmp_path / "test.py"
    nb_path.write_text(notebook)
    out_path = tmp_path / "out.py"

    transform_notebook(
        nb_path,
        output_path=out_path,
        prepend_markdown="Warning",
        move_imports_to_top=True
    )

    result = out_path.read_text()

    # Order: warning < import mo < x
    warning_pos = result.find("Warning")
    import_pos = result.find("import marimo as mo")
    x_pos = result.find("x = 1")

    assert warning_pos < import_pos 
    assert import_pos < x_pos


def test_transform_notebook_preserves_preamble(tmp_path):
    """Preamble (metadata, app setup, __main__) should not be corrupted."""
    notebook = '''import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    x = 1
    return x,


if __name__ == "__main__":
    app.run()
'''
    nb_path = tmp_path / "test.py"
    nb_path.write_text(notebook)
    out_path = tmp_path / "out.py"

    transform_notebook(nb_path, output_path=out_path, prepend_markdown="Test")

    result = out_path.read_text()

    assert '__generated_with = "0.9.0"' in result
    assert 'app = marimo.App(width="full")' in result
    assert 'if __name__ == "__main__":' in result


def test_transform_notebook_overwrites_when_no_output_path(tmp_path):
    """Should modify in-place when output_path is None."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    x = 1
    return x,
'''
    nb_path = tmp_path / "test.py"
    nb_path.write_text(notebook)

    transform_notebook(nb_path, prepend_markdown="Modified")

    result = nb_path.read_text()
    assert "Modified" in result


def test_prepend_markdown_with_special_characters():
    """Markdown with quotes, backticks shouldn't break the cell."""
    notebook = '''import marimo
app = marimo.App()

@app.cell
def __():
    pass
'''
    markdown = 'Here\'s a "test" with `code` and\nmultiline'
    result = prepend_markdown(notebook, markdown)

    assert 'Here\'s a "test"' in result
    assert '`code`' in result
