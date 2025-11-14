from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.config import Config

from .builder import MarimoBuilder
from .directives import MarimoDirective
from .static import setup_static_files
from importlib.metadata import version

def config_inited(app: Sphinx, config: Config) -> None:
    if not hasattr(config, "marimo_notebook_dir"):
        config.marimo_notebook_dir = "notebooks"

    if not hasattr(config, "marimo_build_dir"):
        config.marimo_build_dir = "_build/marimo"

    if not hasattr(config, "marimo_output_dir"):
        config.marimo_output_dir = "_static/marimo"

    # Parallel build and caching defaults
    if not hasattr(config, "marimo_parallel_build"):
        config.marimo_parallel_build = True

    if not hasattr(config, "marimo_n_jobs"):
        config.marimo_n_jobs = -1

    if not hasattr(config, "marimo_cache_notebooks"):
        config.marimo_cache_notebooks = True

    # Click-to-load configuration
    if not hasattr(config, "marimo_click_to_load"):
        config.marimo_click_to_load = True

    if not hasattr(config, "marimo_load_button_text"):
        config.marimo_load_button_text = "Load Interactive Notebook"


def build_marimo_notebooks(app: Sphinx) -> None:
    # Static files go directly in _static/marimo in the build output
    static_dir = Path(app.outdir) / "_static" / "marimo"

    # Setup cache directory if caching is enabled
    cache_dir = None
    if app.config.marimo_cache_notebooks:
        cache_dir = Path(app.outdir) / "_build" / ".marimo_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

    # Build regular Marimo notebooks from marimo directive
    builder = MarimoBuilder(
        source_dir=Path(app.srcdir) / app.config.marimo_notebook_dir,
        build_dir=Path(app.outdir) / app.config.marimo_build_dir,
        static_dir=static_dir,
        parallel_build=app.config.marimo_parallel_build,
        n_jobs=app.config.marimo_n_jobs,
        cache_dir=cache_dir,
    )

    builder.build_all_notebooks()

    setup_static_files(app, static_dir)


def setup(app: Sphinx) -> Dict[str, Any]:
    # Regular Marimo configuration
    app.add_config_value("marimo_notebook_dir", "notebooks", "html")
    app.add_config_value("marimo_build_dir", "_build/marimo", "html")
    app.add_config_value("marimo_output_dir", "_static/marimo", "html")
    app.add_config_value("marimo_default_height", "600px", "html")
    app.add_config_value("marimo_default_width", "100%", "html")

    # Parallel build and caching configuration
    app.add_config_value("marimo_parallel_build", True, "html")
    app.add_config_value("marimo_n_jobs", -1, "html")
    app.add_config_value("marimo_cache_notebooks", True, "html")

    # Click-to-load configuration
    app.add_config_value("marimo_click_to_load", True, "html")
    app.add_config_value("marimo_load_button_text", "Load Interactive Notebook", "html")

    app.add_directive("marimo", MarimoDirective)

    # Event hooks
    app.connect("config-inited", config_inited)
    app.connect("builder-inited", build_marimo_notebooks)

    # Static assets
    app.add_css_file("marimo/marimo-embed.css")
    app.add_js_file("marimo/marimo-loader.js")

    return {
        "version": version("sphinx-marimo"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }