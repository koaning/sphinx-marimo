import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional

from joblib import Parallel, delayed, Memory
from sphinx.util import logging as sphinx_logging

logger = sphinx_logging.getLogger(__name__)


class MarimoBuilder:
    def __init__(
        self,
        source_dir: Path,
        build_dir: Path,
        static_dir: Path,
        parallel_build: bool = True,
        n_jobs: int = -1,
        cache_dir: Optional[Path] = None,
    ) -> None:
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.static_dir = static_dir
        self.parallel_build = parallel_build
        self.n_jobs = n_jobs
        self.notebooks: List[Dict[str, str]] = []

        # Setup caching
        self.memory: Optional[Memory] = None
        if cache_dir:
            self.memory = Memory(cache_dir, verbose=0)

    def build_all_notebooks(self) -> None:
        logger.info(f"Building Marimo notebooks...")
        logger.info(f"  Source dir: {self.source_dir}")
        logger.info(f"  Static dir: {self.static_dir}")

        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)

        notebook_output_dir = self.static_dir / "notebooks"
        notebook_output_dir.mkdir(parents=True, exist_ok=True)

        if self.source_dir.exists():
            notebook_files = list(self.source_dir.glob("**/*.py"))
            logger.info(f"  Found {len(notebook_files)} notebooks")

            if self.parallel_build and len(notebook_files) > 0:
                logger.info(f"  Building in parallel with {self.n_jobs} jobs")
                # Use generator mode to get results as they complete
                total = len(notebook_files)
                completed = 0
                start_time = time.time()

                for result in Parallel(n_jobs=self.n_jobs, return_as="generator")(
                    delayed(self._build_notebook)(notebook_path, notebook_output_dir)
                    for notebook_path in notebook_files
                ):
                    if result:
                        self.notebooks.append(result)
                        completed += 1
                        elapsed = time.time() - start_time
                        avg_time = elapsed / completed
                        remaining = total - completed
                        eta = avg_time * remaining
                        logger.info(
                            f"  Built notebook {completed}/{total}: {result['path']} "
                            f"(avg: {avg_time:.1f}s/notebook, ETA: {eta:.0f}s)"
                        )
            else:
                # Sequential build
                total = len(notebook_files)
                start_time = time.time()

                for i, notebook_path in enumerate(notebook_files, 1):
                    result = self._build_notebook(notebook_path, notebook_output_dir)
                    if result:
                        self.notebooks.append(result)
                        elapsed = time.time() - start_time
                        avg_time = elapsed / i
                        remaining = total - i
                        eta = avg_time * remaining
                        logger.info(
                            f"  Built notebook {i}/{total}: {result['path']} "
                            f"(avg: {avg_time:.1f}s/notebook, ETA: {eta:.0f}s)"
                        )
        else:
            logger.warning(f"  Source directory does not exist: {self.source_dir}")

        self._generate_manifest()
        self._copy_marimo_runtime()

    def _build_notebook(self, notebook_path: Path, output_dir: Path) -> Optional[Dict[str, str]]:
        """Build a single notebook, with optional caching."""
        if self.memory:
            # Use cached version if available
            return self._build_notebook_cached(notebook_path, output_dir)
        else:
            # Build without caching
            return self._build_notebook_impl(notebook_path, output_dir)

    def _build_notebook_cached(self, notebook_path: Path, output_dir: Path) -> Optional[Dict[str, str]]:
        """Cached version of notebook building."""
        # Use memory.cache to wrap the build function
        cached_build = self.memory.cache(self._build_notebook_impl)
        return cached_build(notebook_path, output_dir)

    def _build_notebook_impl(
        self,
        notebook_path: Path,
        output_dir: Path,
    ) -> Optional[Dict[str, str]]:
        """Internal implementation of notebook building."""
        relative_path = notebook_path.relative_to(self.source_dir)
        output_name = str(relative_path).replace("/", "_").replace(".py", "")
        output_path = output_dir / f"{output_name}.html"

        subprocess.run(
            ["marimo", "export", "html-wasm", str(notebook_path), "-o", str(output_path), "--force"],
            check=True,
        )

        notebook_dict = {
            "name": output_name,
            "path": str(relative_path),
            "output": f"notebooks/{output_name}.html",
        }

        return notebook_dict
    def _create_placeholder(self, output_path: Path, source_path: Path) -> None:
        placeholder_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Marimo Notebook - {source_path}</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .placeholder {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        h2 {{ color: #333; margin-bottom: 1rem; }}
        p {{ color: #666; }}
        code {{
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="placeholder">
        <h2>Marimo Notebook</h2>
        <p>Source: <code>{source_path}</code></p>
        <p>To build this notebook, install marimo and rebuild the documentation.</p>
    </div>
</body>
</html>
"""
        output_path.write_text(placeholder_html)

    def _generate_manifest(self) -> None:
        manifest_path = self.static_dir / "manifest.json"
        manifest = {
            "notebooks": self.notebooks,
            "version": "0.1.0",
        }
        manifest_path.write_text(json.dumps(manifest, indent=2))

    def _copy_marimo_runtime(self) -> None:
        runtime_dir = self.static_dir / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)

        try:
            marimo_wasm_path = self._find_marimo_wasm_assets()
            if marimo_wasm_path and marimo_wasm_path.exists():
                for item in marimo_wasm_path.iterdir():
                    if item.is_file():
                        shutil.copy2(item, runtime_dir / item.name)
                    elif item.is_dir():
                        shutil.copytree(item, runtime_dir / item.name, dirs_exist_ok=True)
        except Exception as e:
            logger.info(f"Note: Could not copy marimo runtime assets: {e}")
            self._create_runtime_placeholder(runtime_dir)

    def _find_marimo_wasm_assets(self) -> Optional[Path]:
        try:
            import marimo
            marimo_path = Path(marimo.__file__).parent
            wasm_path = marimo_path / "_static" / "wasm"
            if wasm_path.exists():
                return wasm_path
        except ImportError:
            pass
        return None

    def _create_runtime_placeholder(self, runtime_dir: Path) -> None:
        placeholder_js = """
// Marimo WASM runtime placeholder
console.log('Marimo WASM runtime would be loaded here');
window.MarimoRuntime = {
    init: function() {
        console.log('Initializing Marimo runtime...');
    }
};
"""
        (runtime_dir / "marimo-wasm.js").write_text(placeholder_js)