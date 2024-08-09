from dataclasses import dataclass

from ..collections.types import StationStatusType


@dataclass(init=False)
class Filters:
    __slots__ = ("status", "name", "info",)

    status: StationStatusType
    name: str
    info: str

    def __init__(
            self,
            status: StationStatusType = StationStatusType.All,
            name: str = "",
            info: str = "",
    ):
        self.status = status
        self.name = name
        self.info = info
