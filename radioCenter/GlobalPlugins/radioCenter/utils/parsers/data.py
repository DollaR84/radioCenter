from dataclasses import dataclass
from typing import List


@dataclass(init=False)
class ItemData:
    __slots__ = ("name", "url", "info",)

    name: str
    url: str
    info: List[str]

    def __init__(
            self,
            name: str,
            url: str,
            info: List[str] = [],
    ):
        self.name = name
        self.url = url
        self.info = info

    def add_info(self, *infos):
        for info in infos:
            self.info.append(info)
