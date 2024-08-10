from typing import List, Optional

from .base import BaseParser

from .data import ItemData


class M3UParser(BaseParser):

    def __init__(self, url: str, name: Optional[str] = None):
        self.url: str = url
        self.name = name

        if not name:
            self.name = self.url.rsplit(r"/", 1)[1].replace(".m3u", "")
            print(self.name)

    def get_data(self) -> List[ItemData]:
        results = []
        data = self.get_request(self.url)
        urls = []

        for line in data.splitlines():
            line = line.strip()
            line_start = line[:4]

            if line_start.lower().startswith("http"):
                urls.append(line)

        for url in urls:
            results.append(ItemData(name=self.name, url=url))

        return results
