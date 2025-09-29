from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.config import Config

from .builder import MarimoBuilder
from .directives import MarimoDirective
from .static import setup_static_files

__version__ = "0.1.0"


def config_inited(app: Sphinx, config: Config) -> None:
    if not hasattr(config, "marimo_notebook_dir"):
        config.marimo_notebook_dir = "notebooks"

    if not hasattr(config, "marimo_build_dir"):
        config.marimo_build_dir = "_build/marimo"

    if not hasattr(config, "marimo_output_dir"):
        config.marimo_output_dir = "_static/marimo"


def build_marimo_notebooks(app: Sphinx) -> None:
    # Static files go directly in _static/marimo in the build output
    static_dir = Path(app.outdir) / "_static" / "marimo"

    builder = MarimoBuilder(
        source_dir=Path(app.srcdir) / app.config.marimo_notebook_dir,
        build_dir=Path(app.outdir) / app.config.marimo_build_dir,
        static_dir=static_dir,
    )

    builder.build_all_notebooks()

    setup_static_files(app, static_dir)


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_config_value("marimo_notebook_dir", "notebooks", "html")
    app.add_config_value("marimo_build_dir", "_build/marimo", "html")
    app.add_config_value("marimo_output_dir", "_static/marimo", "html")
    app.add_config_value("marimo_default_height", "600px", "html")
    app.add_config_value("marimo_default_width", "100%", "html")

    app.add_directive("marimo", MarimoDirective)

    app.connect("config-inited", config_inited)
    app.connect("builder-inited", build_marimo_notebooks)

    app.add_css_file("marimo/marimo-embed.css")
    app.add_js_file("marimo/marimo-loader.js")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }