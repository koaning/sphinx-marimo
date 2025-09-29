"""Integration with Sphinx Gallery for Marimo launch buttons."""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import json
import logging

from sphinx.application import Sphinx
from sphinx.util import logging as sphinx_logging

logger = sphinx_logging.getLogger(__name__)


class GalleryMarimoIntegration:
    """Handles integration between Sphinx Gallery and Marimo notebooks."""

    def __init__(self, app: Sphinx):
        self.app = app
        self.gallery_detected = False
        self.gallery_notebooks_dir: Optional[Path] = None
        self.marimo_gallery_dir: Optional[Path] = None

    def detect_sphinx_gallery(self) -> bool:
        """Check if Sphinx Gallery is enabled in this project."""
        try:
            # Check if sphinx_gallery is in extensions
            if 'sphinx_gallery.gen_gallery' not in self.app.config.extensions:
                return False

            # Check if sphinx_gallery_conf exists
            gallery_conf = getattr(self.app.config, 'sphinx_gallery_conf', {})
            if not gallery_conf:
                return False

            self.gallery_detected = True
            logger.info("Sphinx Gallery detected - Marimo launcher will be enabled")
            return True

        except Exception as e:
            logger.debug(f"Gallery detection failed: {e}")
            return False

    def setup_gallery_directories(self) -> None:
        """Setup directory paths for Gallery-generated notebooks and Marimo output."""
        if not self.gallery_detected:
            return

        # Gallery puts notebooks in _downloads directory with hash-based subdirectories
        # We'll search for all .ipynb files in _downloads
        self.gallery_notebooks_dir = Path(self.app.outdir) / "_downloads"

        # Our Marimo output directory
        self.marimo_gallery_dir = Path(self.app.outdir) / "_static" / "marimo" / "gallery"
        self.marimo_gallery_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Gallery notebooks search: {self.gallery_notebooks_dir}")
        logger.info(f"Marimo output: {self.marimo_gallery_dir}")

    def convert_gallery_notebooks(self) -> Dict[str, str]:
        """Convert Gallery-generated .ipynb files to Marimo WASM notebooks."""
        converted_notebooks = {}

        if not self.gallery_detected or not self.gallery_notebooks_dir:
            return converted_notebooks

        if not self.gallery_notebooks_dir.exists():
            logger.warning(f"Gallery notebooks directory not found: {self.gallery_notebooks_dir}")
            return converted_notebooks

        # Find all .ipynb files in Gallery output
        ipynb_files = list(self.gallery_notebooks_dir.rglob("*.ipynb"))
        logger.info(f"Found {len(ipynb_files)} Gallery notebooks to convert")

        for ipynb_file in ipynb_files:
            try:
                converted_path = self._convert_single_notebook(ipynb_file)
                if converted_path:
                    # Store relative path from static root for web access
                    rel_path = converted_path.relative_to(Path(self.app.outdir) / "_static")
                    converted_notebooks[ipynb_file.stem] = str(rel_path)

            except Exception as e:
                logger.error(f"Failed to convert {ipynb_file.name}: {e}")
                continue

        # Save manifest of converted notebooks
        self._save_gallery_manifest(converted_notebooks)

        logger.info(f"Successfully converted {len(converted_notebooks)} Gallery notebooks to Marimo")
        return converted_notebooks

    def _convert_single_notebook(self, ipynb_file: Path) -> Optional[Path]:
        """Convert a single .ipynb file to Marimo WASM format."""
        # Create output paths
        notebook_name = ipynb_file.stem
        marimo_py_file = self.marimo_gallery_dir / f"{notebook_name}.py"
        marimo_html_file = self.marimo_gallery_dir / f"{notebook_name}.html"

        try:
            # Step 1: Convert .ipynb to Marimo .py format
            result = subprocess.run([
                'marimo', 'convert', str(ipynb_file),
                '-o', str(marimo_py_file)
            ], capture_output=True, text=True, check=True)

            logger.debug(f"Converted {ipynb_file.name} to Marimo format")

            # Step 2: Export Marimo notebook to WASM HTML
            result = subprocess.run([
                'marimo', 'export', 'html-wasm', '--mode', 'edit', str(marimo_py_file),
                '-o', str(marimo_html_file)
            ], capture_output=True, text=True, check=True)

            logger.debug(f"Exported {notebook_name} to WASM HTML")
            return marimo_html_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Marimo command failed for {ipynb_file.name}: {e.stderr}")
            return None
        except FileNotFoundError:
            logger.error("marimo command not found - make sure marimo is installed and in PATH")
            return None

    def _save_gallery_manifest(self, converted_notebooks: Dict[str, str]) -> None:
        """Save manifest of converted Gallery notebooks."""
        manifest = {
            "gallery_notebooks": converted_notebooks,
            "total_count": len(converted_notebooks)
        }

        manifest_path = self.marimo_gallery_dir / "gallery_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        logger.debug(f"Saved Gallery manifest with {len(converted_notebooks)} notebooks")

    def should_inject_launcher(self, docname: str) -> bool:
        """Check if a Marimo launcher should be injected for this document."""
        if not self.gallery_detected:
            return False

        # Check if this document is part of a Gallery
        gallery_conf = getattr(self.app.config, 'sphinx_gallery_conf', {})
        gallery_dirs = gallery_conf.get('gallery_dirs', [])

        # Simple check: if docname starts with any gallery directory name
        for gallery_dir in gallery_dirs:
            if docname.startswith(gallery_dir):
                return True

        return False

    def get_notebook_info(self, docname: str) -> Optional[Dict[str, Any]]:
        """Get information about the Marimo notebook for this document."""
        if not self.marimo_gallery_dir or not self.should_inject_launcher(docname):
            return None

        # Try to find corresponding notebook
        notebook_name = Path(docname).name  # Get filename without path
        manifest_path = self.marimo_gallery_dir / "gallery_manifest.json"

        if not manifest_path.exists():
            return None

        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)

            if notebook_name in manifest.get('gallery_notebooks', {}):
                return {
                    'notebook_name': notebook_name,
                    'notebook_url': f"/_static/{manifest['gallery_notebooks'][notebook_name]}",
                    'button_text': getattr(self.app.config, 'marimo_gallery_button_text', 'launch marimo')
                }

        except Exception as e:
            logger.error(f"Failed to load Gallery manifest: {e}")

        return None