import os

__author__ = "Alexander Rusakevich"
__version_str__ = (
    open(os.path.join(os.path.dirname(__file__), "VERSION.txt"), "r").read().strip()
)
__version__ = tuple(int(i) for i in __version_str__.split("."))
