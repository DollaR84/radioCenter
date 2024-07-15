from logHandler import log

from .base import BaseCollection

from ..data import ItemData, CollectionData

from ...pyradios import RadioBrowser


class RadioBrowserCollection(BaseCollection):
    order_id: int = 1

    def __init__(self, name: str):
        super().__init__(name)

        self.client: RadioBrowser = RadioBrowser()

    def make_url(self) -> str:
        return ""

    def load(self, url: str) -> list[ItemData]:
        results = []

        for data in self.client.stations():
            item = ItemData(
                name=data.get("name", "").replace("\t", "").replace("\n", ""),
                url=data.get("url", ""),
            )
            item.add_info(data.get("country"), data.get("countrycode"), str(data.get("bitrate", 0)), data.get("codec"))
            results.append(item)

        return results

    def process_data(self, url: str) -> list[CollectionData]:
        results = []
        try:
            data = self.load(url)
            for item in data:
                results.append(self.read(item))

        except Exception as error:
            log.error(error, exc_info=True)

        return results

    def read(self, item: ItemData) -> CollectionData:
        result = CollectionData(name=item.name)
        result.add(item.url)
        result.add_info(*item.info)
        return result
