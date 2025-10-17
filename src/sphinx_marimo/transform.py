"""Transform Marimo notebook files by manipulating cells."""

import re
from pathlib import Path
from typing import List, Tuple, Optional


def _parse_notebook(content: str) -> Tuple[str, List[str], str]:
    """
    Parse notebook content into preamble, cells, and postamble.

    Args:
        content: The notebook file content

    Returns:
        Tuple of (preamble, list of cells, postamble)
    """
    # Split on @app.cell but keep the decorator with each cell
    parts = re.split(r'(@app\.cell(?:\([^)]*\))?)', content)

    # parts[0] is the preamble (imports, app setup, etc.)
    preamble = parts[0] if parts else ""

    # Combine decorators with their cell content
    cells = []
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            cell_content = parts[i + 1]
            # Check if this is the last part and contains if __name__
            if i + 2 >= len(parts) and 'if __name__' in cell_content:
                # Split off the if __name__ block
                cell_lines = cell_content.split('\n')
                actual_cell_lines = []
                postamble_lines = []
                in_postamble = False

                for line in cell_lines:
                    if line.strip().startswith('if __name__'):
                        in_postamble = True

                    if in_postamble:
                        postamble_lines.append(line)
                    else:
                        actual_cell_lines.append(line)

                if actual_cell_lines:
                    cell = parts[i] + '\n'.join(actual_cell_lines)
                    cells.append(cell)

                postamble = '\n'.join(postamble_lines)
                return preamble, cells, postamble
            else:
                cell = parts[i] + cell_content
                cells.append(cell)
        elif i < len(parts):
            # Last decorator without content
            cells.append(parts[i])

    return preamble, cells, ""


def _create_markdown_cell(markdown_content: str) -> str:
    """
    Create a markdown cell with the given content.

    Args:
        markdown_content: The markdown text to include

    Returns:
        String containing two cells: import cell and markdown display cell
    """
    return f'''@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        {markdown_content}
        """
    )
    return


'''


def prepend_markdown(content: str, markdown_text: str) -> str:
    """
    Prepend a markdown cell to the notebook content.

    Args:
        content: The original notebook content
        markdown_text: The markdown text to prepend

    Returns:
        Transformed notebook content
    """
    preamble, cells, postamble = _parse_notebook(content)

    # Check if there's already an import marimo cell we can reuse
    has_mo_import = any(re.search(r'\bimport\s+marimo\s+as\s+mo\b', cell) for cell in cells)

    if has_mo_import:
        # Just add the markdown display cell, reuse existing import
        markdown_cell = f'''@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        {markdown_text}
        """
    )
    return


'''
    else:
        # Add both import and markdown cells
        markdown_cell = _create_markdown_cell(markdown_text)

    cells.insert(0, markdown_cell)
    return preamble + "".join(cells) + postamble


def move_imports_to_top(content: str) -> str:
    """
    Move all cells containing 'import marimo' to the top.

    Args:
        content: The original notebook content

    Returns:
        Transformed notebook content with imports first
    """
    preamble, cells, postamble = _parse_notebook(content)

    import_cells = []
    other_cells = []

    for cell in cells:
        if re.search(r'\bimport\s+marimo\b', cell):
            import_cells.append(cell)
        else:
            other_cells.append(cell)

    # Reorder: import cells first, then other cells
    cells = import_cells + other_cells
    return preamble + "".join(cells) + postamble


def transform_notebook(
    notebook_path: Path,
    output_path: Optional[Path] = None,
    prepend_markdown: Optional[str] = None,
    move_imports_to_top: bool = False,
) -> Path:
    """
    Transform a Marimo notebook with the specified operations.

    Args:
        notebook_path: Path to the input notebook
        output_path: Path to save the transformed notebook (None = overwrite)
        prepend_markdown: Markdown content to prepend as first cell
        move_imports_to_top: Whether to move import marimo cells to top

    Returns:
        Path to the transformed notebook file
    """
    content = notebook_path.read_text()

    if prepend_markdown:
        content = globals()['prepend_markdown'](content, prepend_markdown)

    if move_imports_to_top:
        content = globals()['move_imports_to_top'](content)

    target_path = output_path or notebook_path
    target_path.write_text(content)
    return target_path
