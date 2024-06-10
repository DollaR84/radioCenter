import os
os.add_dll_directory(os.path.join(os.path.dirname(__file__), "lib"))

from .main import GlobalPlugin


__all__ = [
    "GlobalPlugin",
]
