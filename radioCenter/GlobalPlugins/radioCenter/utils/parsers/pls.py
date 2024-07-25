from typing import List

from .base import BaseParser

from .data import ItemData


class PLSParser(BaseParser):

    def __init__(self, url: str):
        self.url: str = url

    def get_data(self) -> List[ItemData]:
        results = []
        data = self.get_request(self.url)
        urls = {}
        titles = {}

        for line in data.splitlines():
            line = line.strip()

            if line.startswith("File"):
                var, url = line.split("=")
                index = var.replace("File", "")
                urls[index] = url

            if line.startswith("Title"):
                var, title = line.split("=")
                index = var.replace("Title", "")
                titles[index] = title

        for index, url in urls.items():
            title = titles.get(index, "")

            results.append(ItemData(name=title, url=url))

        return results
