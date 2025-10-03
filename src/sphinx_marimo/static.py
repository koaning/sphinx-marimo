from pathlib import Path
import shutil

from sphinx.application import Sphinx


def setup_static_files(app: Sphinx, static_dir: Path) -> None:
    """Copy static CSS and JS files to the Sphinx build directory."""
    # Get the package's static directory
    package_static_dir = Path(__file__).parent / "static"

    # Copy CSS files
    css_source = package_static_dir / "css"
    for css_file in css_source.glob("*.css"):
        shutil.copy2(css_file, static_dir / css_file.name)

    # Copy JS files
    js_source = package_static_dir / "js"
    for js_file in js_source.glob("*.js"):
        shutil.copy2(js_file, static_dir / js_file.name)
