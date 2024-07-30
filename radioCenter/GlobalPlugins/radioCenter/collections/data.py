from dataclasses import dataclass, field

import wx

from .types import StationStatusType


@dataclass(slots=True)
class CollectionData:
    name: str
    urls: list[str] = field(default_factory=list)
    info_data: list[str] = field(default_factory=list)

    status: StationStatusType = StationStatusType.NotVerified
    _current_url_index: int = 0

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


@dataclass(slots=True)
class CollectionDataExt:
    stations: list[CollectionData]
    current_check_index: int = 0
    _verified: bool = False

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
