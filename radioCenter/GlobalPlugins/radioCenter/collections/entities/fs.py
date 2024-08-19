from typing import List

from .base import BaseCollection

from ..data import CollectionData

from ...utils.parsers import M3UParser
from ...utils.parsers.data import ItemData


class FileSystemCollection(BaseCollection):
    order_id: int = 4

    def __init__(self, name: str, **kwargs):
        super().__init__(name)

        self.config = kwargs.get("config")

    @property
    def is_available(self) -> bool:
        return bool(self.make_url())

    def make_url(self) -> str:
        return self.config.fs_collection_path if self.config else ""

    def load(self, url: str) -> List[ItemData]:
        return []

    def process_data(self, url: str) -> List[CollectionData]:
        results = []
        if not url:
            return results

        parser = M3UParser(base_path=url)
        data = parser.get_data()

        for item in data:
            results.append(self.read(item))

        return results

    def read(self, item: ItemData) -> CollectionData:
        item.name = item.name.strip().replace("_", " ")

        result = CollectionData(name=item.name)
        result.add(item.url)
        result.add_info(*item.info)

        return result
