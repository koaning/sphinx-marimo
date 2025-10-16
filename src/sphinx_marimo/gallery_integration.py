"""Integration with Sphinx Gallery for Marimo launch buttons."""

import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any
import json
import logging

from joblib import Parallel, delayed, Memory
from sphinx.application import Sphinx
from sphinx.util import logging as sphinx_logging

logger = sphinx_logging.getLogger(__name__)


def _convert_notebook_standalone(
    ipynb_file: Path,
    marimo_gallery_dir: Path,
    memory: Optional[Memory],
) -> tuple[Path, Optional[Path]]:
    """Standalone function for parallel notebook conversion."""
    try:
        # Create output paths
        notebook_name = ipynb_file.stem
        marimo_py_file = marimo_gallery_dir / f"{notebook_name}.py"
        marimo_html_file = marimo_gallery_dir / f"{notebook_name}.html"

        # Check cache if available
        if memory:
            cached_convert = memory.cache(_convert_notebook_impl)
            converted_path = cached_convert(ipynb_file, marimo_py_file, marimo_html_file)
        else:
            converted_path = _convert_notebook_impl(ipynb_file, marimo_py_file, marimo_html_file)

        return (ipynb_file, converted_path)
    except Exception as e:
        logger.error(f"Failed to convert {ipynb_file.name}: {e}")
        return (ipynb_file, None)


def _convert_notebook_impl(
    ipynb_file: Path,
    marimo_py_file: Path,
    marimo_html_file: Path,
) -> Optional[Path]:
    """Actual implementation of notebook conversion (cacheable)."""
    try:
        # Step 1: Convert .ipynb to Marimo .py format
        result = subprocess.run(
            ["marimo", "convert", str(ipynb_file), "-o", str(marimo_py_file)],
            check=True,
        )

        logger.debug(f"Converted {ipynb_file.name} to Marimo format")

        # Step 2: Export Marimo notebook to WASM HTML
        result = subprocess.run(
            [
                "marimo",
                "export",
                "html-wasm",
                "--mode",
                "edit",
                str(marimo_py_file),
                "-o",
                str(marimo_html_file),
            ],
            check=True,
        )

        logger.debug(f"Exported {ipynb_file.stem} to WASM HTML")
        return marimo_html_file

    except subprocess.CalledProcessError as e:
        logger.error(f"Marimo command failed for {ipynb_file.name}: {e}")
        return None
    except FileNotFoundError:
        logger.error(
            "marimo command not found - make sure marimo is installed and in PATH"
        )
        return None


class GalleryMarimoIntegration:
    """Handles integration between Sphinx Gallery and Marimo notebooks."""

    def __init__(
        self,
        app: Sphinx,
        parallel_build: Optional[bool] = None,
        n_jobs: Optional[int] = None,
        cache_dir: Optional[Path] = None,
    ):
        self.app = app
        self.gallery_detected = False
        self.gallery_notebooks_dir: Optional[Path] = None
        self.marimo_gallery_dir: Optional[Path] = None

        # Use config values if not explicitly provided
        self.parallel_build = (
            parallel_build
            if parallel_build is not None
            else getattr(app.config, "marimo_parallel_build", True)
        )
        self.n_jobs = (
            n_jobs if n_jobs is not None else getattr(app.config, "marimo_n_jobs", -1)
        )

        # Setup caching
        self.memory: Optional[Memory] = None
        if cache_dir:
            self.memory = Memory(cache_dir, verbose=0)

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

        if self.parallel_build and len(ipynb_files) > 0:
            logger.info(f"Converting in parallel with {self.n_jobs} jobs")
            # Use generator mode to get results as they complete
            # Pass necessary parameters instead of self to avoid pickling issues
            total = len(ipynb_files)
            completed = 0
            start_time = time.time()

            for ipynb_file, converted_path in Parallel(n_jobs=self.n_jobs, return_as="generator")(
                delayed(_convert_notebook_standalone)(
                    ipynb_file,
                    self.marimo_gallery_dir,
                    self.memory
                )
                for ipynb_file in ipynb_files
            ):
                if converted_path:
                    completed += 1
                    elapsed = time.time() - start_time
                    avg_time = elapsed / completed
                    remaining = total - completed
                    eta = avg_time * remaining
                    logger.info(
                        f"Converted {completed}/{total}: {ipynb_file.name} "
                        f"(avg: {avg_time:.1f}s/notebook, ETA: {eta:.0f}s)"
                    )
                    # Store relative path from static root for web access
                    rel_path = converted_path.relative_to(Path(self.app.outdir) / "_static")
                    converted_notebooks[ipynb_file.stem] = str(rel_path)
        else:
            # Sequential conversion
            total = len(ipynb_files)
            start_time = time.time()

            for i, ipynb_file in enumerate(ipynb_files, 1):
                try:
                    _, converted_path = _convert_notebook_standalone(
                        ipynb_file, self.marimo_gallery_dir, self.memory
                    )
                    if converted_path:
                        elapsed = time.time() - start_time
                        avg_time = elapsed / i
                        remaining = total - i
                        eta = avg_time * remaining
                        logger.info(
                            f"Converted {i}/{total}: {ipynb_file.name} "
                            f"(avg: {avg_time:.1f}s/notebook, ETA: {eta:.0f}s)"
                        )
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
                }

        except Exception as e:
            logger.error(f"Failed to load Gallery manifest: {e}")

        return None