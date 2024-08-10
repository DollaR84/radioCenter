from dataclasses import dataclass
from enum import Enum
import json
from typing import List, Union

from .base import BaseCollection

from ..data import CollectionData

from ...bs4 import BeautifulSoup


@dataclass(slots=True)
class ItemData:
    name: str
    path: str
    type: str


class UrlType(Enum):
    DIRECTORY = "directory"
    FILE = "file"


class InternetRadioStreamsCollection(BaseCollection):
    order_id: int = 2

    def __init__(self, name: str):
        super().__init__(name)

        self.base_directory_url: str = "https://github.com/mikepierce/internet-radio-streams/tree"
        self.base_file_url: str = "https://raw.githubusercontent.com/mikepierce/internet-radio-streams"

    def make_url(self, url_type: Union[UrlType, str] = UrlType.DIRECTORY, element_url: str = "") -> str:
        if isinstance(url_type, UrlType):
            url_type = url_type.value
        return "/".join([getattr(self, f"base_{url_type}_url"), "main", element_url])

    def load(self, url: str) -> List[ItemData]:
        results = []
        search_data = []
        content = self.get_request(url)

        bs = BeautifulSoup(content, "html.parser")
        search1 = bs.find_all("script", {"type": "application/json", "data-target": "react-partial.embeddedData"})
        if search1:
            search_data.extend(search1)
        search2 = bs.find_all("script", {"type": "application/json", "data-target": "react-app.embeddedData"})
        if search2:
            search_data.extend(search2)

        for repository in search_data:
            if not repository:
                continue
            data = json.loads(repository.text)

            props = data.get("props")
            if props:
                payload = props.get("initialPayload")
            else:
                payload = data.get("payload")
            if not payload:
                continue

            tree = payload.get("tree")
            if not tree:
                continue

            items = tree.get("items", [])
            for item in items:
                name = item.get("name")
                if not name or name in (".github", "README.md",):
                    continue
                name = name.replace(".m3u", "")

                results.append(ItemData(
                    name=name,
                    path=item.get("path"),
                    type=item.get("contentType"),
                ))

        return results

    def process_data(self, url: str) -> List[CollectionData]:
        results = []
        data = self.load(url)

        for item in data:
            if item.type == UrlType.FILE.value:
                results.append(self.read(item))
            elif item.type == UrlType.DIRECTORY.value:
                results.extend(self.process_data(self.make_url(item.type, item.path)))

        return results

    def read(self, item: ItemData) -> CollectionData:
        item.name = item.name.strip().replace("-", " ").replace("_", " ")
        result = CollectionData(name=item.name)
        data = self.get_request(self.make_url(item.type, item.path))

        for line in data.splitlines():
            line = line.strip()
            line_start = line[:4]

            if line_start.lower().startswith("http"):
                result.add(line)

        return result
