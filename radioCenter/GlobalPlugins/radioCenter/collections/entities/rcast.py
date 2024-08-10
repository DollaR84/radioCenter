from typing import List

from logHandler import log

from .base import BaseCollection

from ..data import CollectionData

from ...bs4 import BeautifulSoup

from ...utils.parsers.data import ItemData


class Mp3RadioStationsCollection(BaseCollection):
    order_id: int = 3

    def __init__(self, name: str):
        super().__init__(name)

        self.base_url: str = "https://www.rcast.net/dir/mp3"

        self.current_page: int = 1
        self.last_page: int | None = None

    def make_url(self, page_number: int = 1) -> str:
        return "/".join([self.base_url, f"page{page_number}"])

    def load(self, url: str) -> List[ItemData]:
        results = []
        content = self.get_request(url)

        bs = BeautifulSoup(content, "html.parser")
        table = bs.find("table")

        for row in table.find_all("tr"):
            item = None
            for column in row.find_all("td"):
                title = column.find("h4")
                if not title and not item:
                    continue

                if title:
                    name = title.find("a").text
                    url = column.find("small").find("a").text

                    if all([name, url]):
                        item = ItemData(name=name, url=url)
                        continue
                    else:
                        continue

                else:
                    params = column.find("p")
                    if params:
                        rows = params.text.split("\n")
                        item.add_info(rows[0], rows[2])
                results.append(item)

        if not self.last_page:
            is_disabled = False
            pagination = bs.find("ul", {"class": "pagination"})
            for line in pagination.find_all("li"):
                if "disabled" in line.get("class", []):
                    is_disabled = True
                elif not is_disabled:
                    continue
                else:
                    self.last_page = int(line.find("a").text)
                    break

        return results

    def process_data(self, url: str) -> List[CollectionData]:
        results = []
        try:
            data = self.load(url)
            for item in data:
                results.append(self.read(item))

            self.current_page += 1
            if self.last_page and self.current_page <= self.last_page:
                results.extend(self.process_data(self.make_url(self.current_page)))
        except Exception as error:
            log.error(error, exc_info=True)

        return results

    def read(self, item: ItemData) -> CollectionData:
        result = CollectionData(name=item.name.strip())
        result.add(item.url)
        result.add_info(*item.info)
        return result
