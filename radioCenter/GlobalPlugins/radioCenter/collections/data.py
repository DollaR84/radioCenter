from dataclasses import dataclass
from typing import List

import wx

from .types import StationStatusType


@dataclass(init=False)
class CollectionData:
    __slots__ = ("name", "urls", "info_data", "status", "_current_url_index",)

    name: str
    urls: List[str]
    info_data: List[str]

    status: StationStatusType
    _current_url_index: int

    def __init__(
            self,
            name: str,
            urls: List[str] = [],
            info_data: List[str] = [],
            status: StationStatusType = StationStatusType.NotVerified,
            current_url_index: int = 0,
    ):
        self.name = name
        self.urls = urls
        self.info_data = info_data
        self.status = status
        self._current_url_index = current_url_index

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


@dataclass(init=False)
class CollectionDataExt:
    __slots____ = ("stations", "current_check_index", "_verified",)

    stations: List[CollectionData]
    current_check_index: int
    _verified: bool

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
            station = self.stations[self.current_check_index]
            if self._verified:
                self.current_check_index += 1
                self._verified = False
            return station

        else:
            raise StopIteration

    def verified(self):
        self._verified = True

    @property
    def is_verified(self):
        return self._verified
