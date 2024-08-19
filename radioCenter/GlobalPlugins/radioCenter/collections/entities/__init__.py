from .base import BaseCollection
from .fs import FileSystemCollection
from .irs import InternetRadioStreamsCollection
from .rcast import Mp3RadioStationsCollection
from .rb import RadioBrowserCollection


__all__ = [
    "BaseCollection",
    "FileSystemCollection",
    "InternetRadioStreamsCollection",
    "Mp3RadioStationsCollection",
    "RadioBrowserCollection",
]
