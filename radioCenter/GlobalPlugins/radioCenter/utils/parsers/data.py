from dataclasses import dataclass, field
import sys
from typing import List


@dataclass(**({"slots": True} if sys.version_info >= (3, 10) else {}))
class ItemData:
    name: str
    url: str
    info: List[str] = field(default_factory=list)

    def add_info(self, *infos):
        for info in infos:
            self.info.append(info)
