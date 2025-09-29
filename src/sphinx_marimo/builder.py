import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class MarimoBuilder:
    def __init__(self, source_dir: Path, build_dir: Path, static_dir: Path) -> None:
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.static_dir = static_dir
        self.notebooks: List[Dict[str, str]] = []

    def build_all_notebooks(self) -> None:
        print(f"Building Marimo notebooks...")
        print(f"  Source dir: {self.source_dir}")
        print(f"  Static dir: {self.static_dir}")

        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)

        notebook_output_dir = self.static_dir / "notebooks"
        notebook_output_dir.mkdir(parents=True, exist_ok=True)

        if self.source_dir.exists():
            notebook_files = list(self.source_dir.glob("**/*.py"))
            print(f"  Found {len(notebook_files)} notebooks")

            for notebook_path in notebook_files:
                self._build_notebook(notebook_path, notebook_output_dir)
        else:
            print(f"  Warning: Source directory does not exist: {self.source_dir}")

        self._generate_manifest()
        self._copy_marimo_runtime()

    def _build_notebook(self, notebook_path: Path, output_dir: Path) -> None:
        relative_path = notebook_path.relative_to(self.source_dir)
        output_name = str(relative_path).replace("/", "_").replace(".py", "")
        output_path = output_dir / f"{output_name}.html"

        try:
            result = subprocess.run(
                ["marimo", "export", "html-wasm", str(notebook_path), "-o", str(output_path), "--force"],
                capture_output=True,
                text=True,
                check=True,
            )

            self.notebooks.append({
                "name": output_name,
                "path": str(relative_path),
                "output": f"notebooks/{output_name}.html",
            })

            print(f"Built notebook: {relative_path}")

        except subprocess.CalledProcessError as e:
            print(f"Failed to build notebook {notebook_path}: {e.stderr}")
        except FileNotFoundError:
            print("Warning: marimo command not found. Skipping WASM build.")
            self._create_placeholder(output_dir / f"{output_name}.html", relative_path)

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
            print(f"Note: Could not copy marimo runtime assets: {e}")
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