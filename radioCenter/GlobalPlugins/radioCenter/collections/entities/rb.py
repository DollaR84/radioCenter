﻿import sys
from typing import List

from logHandler import log

from .base import BaseCollection

from ..data import CollectionData

from ...pyradios import RadioBrowser

from ...utils.parsers.data import ItemData


class RadioBrowserCollection(BaseCollection):
    order_id: int = 1

    def __init__(self, name: str, **kwargs):
        super().__init__(name)

        self.client: RadioBrowser = RadioBrowser()

    @property
    def is_available(self) -> bool:
        return sys.version_info >= (3, 10)

    def make_url(self) -> str:
        return ""

    def load(self, url: str) -> List[ItemData]:
        results = []

        for data in self.client.stations():
            item = ItemData(
                name=data.get("name", "").replace("\t", "").replace("\n", ""),
                url=data.get("url", ""),
            )
            item.add_info(data.get("country"), data.get("countrycode"), str(data.get("bitrate", 0)), data.get("codec"))
            results.append(item)

        return results

    def process_data(self, url: str) -> List[CollectionData]:
        results = []
        try:
            data = self.load(url)
            for item in data:
                results.append(self.read(item))

        except Exception as error:
            log.error(error, exc_info=True)

        return results

    def read(self, item: ItemData) -> CollectionData:
        result = CollectionData(name=item.name.strip())
        result.add(item.url)
        result.add_info(*item.info)
        return result
