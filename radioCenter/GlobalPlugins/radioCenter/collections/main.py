﻿from concurrent.futures import ThreadPoolExecutor, Future, as_completed
import json
from typing import Callable, Optional

import wx

from .entities import BaseCollection

from .data import CollectionData, CollectionDataExt

from .types import StationStatusType

from ..player import Player

from ..tester import RadioTestData, RadioTester

from ..types import SoundType


class RadioCollections:

    def __init__(self):
        self.collections: BaseCollection = BaseCollection

        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self._future: Optional[Future] = None

    @property
    def collections_names(self) -> list[str]:
        return self.collections.get_collections_names()

    def get_collection(self, name: str) -> BaseCollection:
        return self.collections.get_collection(name)

    def update(self, collection: BaseCollection, callback_finish: Callable):
        if self._future is not None:
            self._future = None

        self._future = self._executor.submit(collection.parse)
        wx.CallLater(1000, self.check, collection.name, callback_finish)

    def check(self, collection_name: str, callback_finish: Callable):
        if self._future.done():
            data = self._future.result()
            Player.play(SoundType.Success)
            callback_finish(collection_name, data)

        else:
            Player.play(SoundType.Move)
            wx.CallLater(1000, self.check, collection_name, callback_finish)

    def verify(self, collection_data: CollectionData, index: int, repeat_count: int, callback_after: Callable):
        if self._future is not None:
            self._future = None

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = {
                executor.submit(
                    self.verify_station,
                    collection_data,
                    index,
                    repeat_count,
                    callback_after,
                ): index
            }
            for future in as_completed(futures):
                futures.pop(future)

    def verify_station(self, collection_data: CollectionData, index: int, repeat_count: int, callback_after: Callable):
        data = RadioTestData(
            callback_after=callback_after, url=collection_data.url,
            name=collection_data.name, station_index=index,
        )
        RadioTester(data, repeat_count, is_speech_mode=False)
