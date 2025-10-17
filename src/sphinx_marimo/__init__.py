from importlib.metadata import version

from .extension import setup

__version__ = version("sphinx-marimo")

__all__ = ["setup", "__version__"]
