import os

try:
    os.add_dll_directory(os.path.join(os.path.dirname(__file__), "lib"))
except Exception:
    os.environ["PATH"] = os.path.join(os.path.dirname(__file__), "lib") + os.pathsep + os.environ["PATH"]

from .main import GlobalPlugin


__all__ = [
    "GlobalPlugin",
]
