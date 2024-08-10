from dataclasses import dataclass

from ..collections.types import StationStatusType


@dataclass(init=False)
class Filters:
    __slots__ = ("status", "_name", "_info",)

    status: StationStatusType

    _name: str
    _info: str

    def __init__(
            self,
            status: StationStatusType = StationStatusType.All,
            name: str = "",
            info: str = "",
    ):
        self.status = status
        self._name = name
        self._info = info

    @property
    def name(self) -> str:
        return self._name.lower()

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def info(self) -> str:
        return self._info.lower()

    @info.setter
    def info(self, value: str):
        self._info = value
