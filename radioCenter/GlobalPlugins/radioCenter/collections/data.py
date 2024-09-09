from dataclasses import dataclass, field
import sys
from typing import Any, Dict, List, Union

import wx

from .types import StationStatusType


@dataclass(**({"slots": True} if sys.version_info >= (3, 10) else {}))
class CollectionData:
    name: str
    urls: List[str] = field(default_factory=list)
    info_data: List[str] = field(default_factory=list)

    status: StationStatusType = StationStatusType.NotVerified
    current_url_index: int = 0

    @property
    def url(self) -> str:
        if len(self.urls) == 1:
            return self.urls[0]
        try:
            return self.urls[self._current_url_index]
        except Exception:
            return ""

    def add(self, url: str):
        self.urls.append(url)

    def add_info(self, *infos):
        for info in infos:
            if info:
                self.info_data.append(info)

    @property
    def info(self) -> str:
        info = ""
        if self.info_data:
            info = "; ".join(self.info_data)
        return info

    @property
    def many_urls_status(self) -> bool:
        return len(self.urls) > 1

    def next_url(self):
        self._current_url_index += 1
        if len(self.urls) <= self._current_url_index:
            self._current_url_index = 0

    def previous_url(self):
        self._current_url_index -= 1
        if self._current_url_index < 0:
            self._current_url_index = len(self.urls) - 1

    def change_url(self, keycode):
        if keycode in (wx.WXK_DOWN, wx.WXK_LEFT,):
            self.previous_url()
            return True

        elif keycode in (wx.WXK_UP, wx.WXK_RIGHT,):
            self.next_url()
            return True

        return False


class CollectionDataExt:
    __slots____ = ("stations", "current_check_index", "_verified",)

    def __init__(
            self,
            stations: List[CollectionData],
            current_check_index: int = 0,
            verified: bool = False,
    ):
        self.stations = stations
        self.current_check_index = current_check_index
        self._verified = verified

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_check_index < len(self.stations) - 1:
            if self._verified:
                self.current_check_index += 1
                self._verified = False

            station = self.stations[self.current_check_index]
            return station

        else:
            raise StopIteration

    def verified(self):
        self._verified = True

    @property
    def is_verified(self):
        return self._verified
