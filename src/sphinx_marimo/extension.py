from pathlib import Path
from typing import Any, Dict

from sphinx.application import Sphinx
from sphinx.config import Config

from .builder import MarimoBuilder
from .directives import MarimoDirective
from .static import setup_static_files
from .gallery_integration import GalleryMarimoIntegration

__version__ = "0.1.0"


def config_inited(app: Sphinx, config: Config) -> None:
    if not hasattr(config, "marimo_notebook_dir"):
        config.marimo_notebook_dir = "notebooks"

    if not hasattr(config, "marimo_build_dir"):
        config.marimo_build_dir = "_build/marimo"

    if not hasattr(config, "marimo_output_dir"):
        config.marimo_output_dir = "_static/marimo"

    # Gallery integration defaults
    if not hasattr(config, "marimo_gallery_button_text"):
        config.marimo_gallery_button_text = "launch marimo"


def build_marimo_notebooks(app: Sphinx) -> None:
    # Static files go directly in _static/marimo in the build output
    static_dir = Path(app.outdir) / "_static" / "marimo"

    # Build regular Marimo notebooks from marimo directive
    builder = MarimoBuilder(
        source_dir=Path(app.srcdir) / app.config.marimo_notebook_dir,
        build_dir=Path(app.outdir) / app.config.marimo_build_dir,
        static_dir=static_dir,
    )

    builder.build_all_notebooks()

    setup_static_files(app, static_dir)


def gallery_build_finished(app: Sphinx, exc) -> None:
    """Hook that runs after Sphinx Gallery has finished building."""
    if exc is not None:
        # Build failed, skip Gallery integration
        return

    gallery_integration = GalleryMarimoIntegration(app)

    # Detect and setup Gallery integration
    if gallery_integration.detect_sphinx_gallery():
        gallery_integration.setup_gallery_directories()
        gallery_integration.convert_gallery_notebooks()


def html_page_context(app: Sphinx, pagename: str, templatename: str, context: dict, doctree) -> None:
    """Inject Marimo launcher information into page context for Gallery pages."""
    gallery_integration = GalleryMarimoIntegration(app)

    notebook_info = gallery_integration.get_notebook_info(pagename)
    if notebook_info:
        context['marimo_notebook_info'] = notebook_info


def setup(app: Sphinx) -> Dict[str, Any]:
    # Regular Marimo configuration
    app.add_config_value("marimo_notebook_dir", "notebooks", "html")
    app.add_config_value("marimo_build_dir", "_build/marimo", "html")
    app.add_config_value("marimo_output_dir", "_static/marimo", "html")
    app.add_config_value("marimo_default_height", "600px", "html")
    app.add_config_value("marimo_default_width", "100%", "html")

    # Gallery integration configuration
    app.add_config_value("marimo_gallery_button_text", "launch marimo", "html")

    app.add_directive("marimo", MarimoDirective)

    # Event hooks
    app.connect("config-inited", config_inited)
    app.connect("builder-inited", build_marimo_notebooks)
    app.connect("build-finished", gallery_build_finished)
    app.connect("html-page-context", html_page_context)

    # Static assets
    app.add_css_file("marimo/marimo-embed.css")
    app.add_js_file("marimo/marimo-loader.js")
    app.add_css_file("marimo/gallery-launcher.css")
    app.add_js_file("marimo/gallery-launcher.js")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }