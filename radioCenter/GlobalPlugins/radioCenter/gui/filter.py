from dataclasses import dataclass

from ..collections.types import StationStatusType


@dataclass(slots=True)
class Filters:
    status: StationStatusType = StationStatusType.All
    name: str = ""
    info: str = ""
