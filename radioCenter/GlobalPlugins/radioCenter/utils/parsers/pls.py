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
            line_start = line[:5]

            if line_start.lower().startswith("file"):
                var, url = line.split("=")
                index = var.lower().replace("file", "")
                urls[index] = url

            if line_start.lower().startswith("title"):
                var, title = line.split("=")
                index = var.lower().replace("title", "")
                titles[index] = title

        for index, url in urls.items():
            title = titles.get(index, "")

            results.append(ItemData(name=title, url=url))

        return results
